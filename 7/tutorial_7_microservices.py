# -*- coding: utf-8 -*-
"""Tutorial 7 microservices.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RNomR0j0sBMyU4B7zBmjqVbeTAvDjmPb
"""

# user_service.py
class UserService:
    def __init__(self):
        self.users = {
            '1': {'id': '1', 'name': 'John Doe', 'email': 'john@example.com'},
            '2': {'id': '2', 'name': 'Jane Doe', 'email': 'jane@example.com'}
        }

    def get_user(self, user_id):
        return self.users.get(user_id, {})

# index_service.py
class IndexService:
    def __init__(self):
        self.documents = {}
        self.index = {}

    def add_document(self, doc_data):
        """Add a document to the index"""
        doc_id = str(len(self.documents) + 1)
        self.documents[doc_id] = {**doc_data, 'id': doc_id}

        # Create inverted index
        words = doc_data['content'].lower().split()
        for word in words:
            if word not in self.index:
                self.index[word] = set()
            self.index[word].add(doc_id)

        return self.documents[doc_id]

    def get_document(self, doc_id):
        """Retrieve a document by ID"""
        return self.documents.get(doc_id)

    def search_word(self, word):
        """Find documents containing a word"""
        word = word.lower()
        return list(self.index.get(word, set()))

# query_service.py
class QueryService:
    def __init__(self, index_service):
        self.index_service = index_service
        self.queries = {}

    def create_query(self, query_data):
        """Create and execute a search query"""
        try:
            query_id = str(len(self.queries) + 1)
            search_terms = query_data['terms']

            # Find matching documents
            results = set()
            for term in search_terms:
                doc_ids = self.index_service.search_word(term)
                if not results:
                    results = set(doc_ids)
                else:
                    results &= set(doc_ids)

            # Create query record
            query = {
                'id': query_id,
                'terms': search_terms,
                'results': list(results),
                'timestamp': query_data.get('timestamp', 'now')
            }
            self.queries[query_id] = query
            return query

        except Exception as e:
            return {'error': str(e)}

# result_service.py
class ResultService:
    def __init__(self, index_service, query_service):
        self.index_service = index_service
        self.query_service = query_service
        self.results = {}

    def format_results(self, query_id):
        """Format search results for display"""
        try:
            query = self.query_service.queries.get(query_id)
            if not query:
                return {'error': 'Query not found'}

            formatted_results = []
            for doc_id in query['results']:
                doc = self.index_service.get_document(doc_id)
                if doc:
                    formatted_results.append({
                        'doc_id': doc_id,
                        'title': doc['title'],
                        'snippet': doc['content'][:100] + '...'
                    })

            result_id = str(len(self.results) + 1)
            result = {
                'id': result_id,
                'query_id': query_id,
                'formatted_results': formatted_results,
                'count': len(formatted_results)
            }
            self.results[result_id] = result
            return result

        except Exception as e:
            return {'error': str(e)}

# main.py
def main():
    # Initialize services
    index_service = IndexService()
    query_service = QueryService(index_service)
    result_service = ResultService(index_service, query_service)

    # Add sample documents
    doc1 = index_service.add_document({
        'title': 'Python Programming',
        'content': 'Python is a popular programming language for cloud computing'
    })
    doc2 = index_service.add_document({
        'title': 'Cloud Services',
        'content': 'Cloud computing enables scalable microservices architecture'
    })
    print(f"Added documents: {doc1['id']}, {doc2['id']}")

    # Create and execute a search query
    query = query_service.create_query({
        'terms': ['cloud', 'computing']
    })
    print(f"Query results: {query}")

    # Format the results
    formatted_results = result_service.format_results(query['id'])
    print(f"Formatted results: {formatted_results}")

if __name__ == "__main__":
    main()

# Example test cases
def test_search():
    # Initialize services
    index_service = IndexService()
    query_service = QueryService(index_service)
    result_service = ResultService(index_service, query_service)

    # Test document indexing
    doc = index_service.add_document({
        'title': 'Test Document',
        'content': 'This is a test document about microservices'
    })
    assert doc['id'] == '1'

    # Test search functionality
    query = query_service.create_query({
        'terms': ['test', 'microservices']
    })
    assert len(query['results']) == 1

    # Test result formatting
    results = result_service.format_results(query['id'])
    assert results['count'] == 1
    assert 'test document' in results['formatted_results'][0]['snippet'].lower()

if __name__ == "__main__":
    test_search()

"""
Function as a Service (FaaS) Architecture Demo: Search Engine Implementation

This code demonstrates key FaaS principles through a simple search engine implementation.
It simulates how serverless functions would operate in a cloud environment.

Key FaaS Characteristics Demonstrated:
1. Stateless Functions - Each invocation is independent
2. Event-Driven Architecture - Functions respond to specific triggers
3. Single Responsibility - Each function performs one specific task
4. Automatic Scaling (simulated) - Functions can handle multiple concurrent requests
"""

class IndexerFunction:

    def __init__(self):
        # In real FaaS, this would be external storage
        self.index = {}

    def handle(self, event):
        """
        Function entry point - similar to AWS Lambda handler

        Args:
            event (dict): Contains document to be indexed
                {
                    'document_id': str - Unique document identifier
                    'content': str - Document content to index
                }

        Returns:
            dict: Indexing operation results
                {
                    'status': str - Operation status
                    'indexed_words': int - Number of words processed
                }
        """
        doc_id = event['document_id']
        content = event['content'].lower().split()

        # Build inverted index
        for word in content:
            if word not in self.index:
                self.index[word] = set()
            self.index[word].add(doc_id)

        return {
            'status': 'success',
            'indexed_words': len(content)
        }

class SearcherFunction:
    """
    Simulates a FaaS search function.

    FaaS Characteristics:
    - Event-driven: Responds to search requests
    - Stateless: Each search is independent
    - Scalable: Multiple instances can handle concurrent searches


    """
    def __init__(self, index_service):
        self.index = index_service.index

    def handle(self, event):
        """
        Search function entry point

        Args:
            event (dict): Contains search parameters
                {
                    'query': str - Search terms
                }

        Returns:
            dict: Search results
                {
                    'status': str - Operation status
                    'results': list - Matching document IDs
                }

        Note: In real FaaS:
        - Would include error handling
        - Would implement timeouts
        - Would include logging/monitoring
        """
        terms = event['query'].lower().split()
        results = set()

        for term in terms:
            if term in self.index:
                if not results:
                    results = self.index[term].copy()
                else:
                    results &= self.index[term]

        return {
            'status': 'success',
            'results': list(results)
        }

class FaaSSimulator:
    """
    Simulates a FaaS environment.

    Demonstrates:
    - Function isolation
    - Event-based invocation
    - Resource management (simulated)
    - Function routing

    In real FaaS platforms (like AWS Lambda):
    - Functions run in isolated containers
    - Resources are automatically managed
    - Scaling happens automatically
    - Includes monitoring and logging
    """
    def __init__(self):
        self.indexer = IndexerFunction()
        self.searcher = SearcherFunction(self.indexer)
        self.invocations = 0

    def invoke(self, function_name, event):
        """
        Simulates FaaS function invocation

        Args:
            function_name (str): Name of function to invoke
            event (dict): Event data for the function

        Real FaaS differences:
        - Would spawn new container/instance
        - Would handle concurrent requests
        - Would implement timeout limits
        - Would include error handling
        """
        self.invocations += 1

        if function_name == 'indexer':
            return self.indexer.handle(event)
        elif function_name == 'searcher':
            return self.searcher.handle(event)
        else:
            raise ValueError(f"Unknown function: {function_name}")

def demonstrate_faas():
    """
    Demonstrates key FaaS concepts through example usage

    Shows:
    1. Event-driven invocation
    2. Function independence
    3. Scalability potential
    """
    # Test data setup
    test_documents = [
        {
            'document_id': 'doc1',
            'content': 'Python is a popular programming language for cloud computing'
        },
        {
            'document_id': 'doc2',
            'content': 'Cloud computing enables scalable microservices architecture'
        }
    ]

    # Initialize FaaS environment
    faas = FaaSSimulator()

    # Demonstrate event-driven invocation
    print("1. Event-Driven Invocation:")
    for doc in test_documents:
        result = faas.invoke('indexer', doc)
        print(f"  Indexed document {doc['document_id']}: {result}")

    # Demonstrate independent function calls
    print("\n2. Independent Function Calls:")
    search_queries = [
        {'query': 'cloud computing'},
        {'query': 'python programming'}
    ]

    for query in search_queries:
        result = faas.invoke('searcher', query)
        print(f"  Search results for '{query['query']}': {result}")

    # Demonstrate scalability concept
    print(f"\n3. Scalability Demonstration:")
    print(f"  Total function invocations: {faas.invocations}")
    print("  In real FaaS: These would execute in parallel with automatic scaling")

if __name__ == "__main__":
    demonstrate_faas()
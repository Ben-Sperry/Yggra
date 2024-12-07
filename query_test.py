import unittest
from datetime import datetime
from graph_layer_core import GraphLayer, EntityType, EntityId
from graph_query_system import GraphQuery, QueryResultType, QueryResult

class TestGraphQuery(unittest.TestCase):
    def setUp(self):
        """
        Creates a test graph with some sample data structure representing a simple
        document management system with tags and categories.
        """
        print("\nSetting up test environment...")
        self.graph = GraphLayer(node_id="test_node")
        
        # Create property types
        print("Creating property types for our test graph...")
        self.type_prop = self.graph.create_entity(EntityType.PROPERTY)
        self.graph.add_label(self.type_prop.id, "type")
        
        self.tag_prop = self.graph.create_entity(EntityType.PROPERTY)
        self.graph.add_label(self.tag_prop.id, "tagged_with")
        
        self.name_prop = self.graph.create_entity(EntityType.PROPERTY)
        self.graph.add_label(self.name_prop.id, "name")
        print("Created properties: type, tagged_with, name")
        
        # Create test documents
        print("\nCreating test documents...")
        self.doc1 = self.graph.create_entity()
        self.graph.add_label(self.doc1.id, "Document 1")
        self.graph.add_statement(self.doc1.id, self.type_prop.id, "document")
        self.graph.add_statement(self.doc1.id, self.name_prop.id, "Project Proposal")
        print("Created Document 1: 'Project Proposal'")
        
        self.doc2 = self.graph.create_entity()
        self.graph.add_label(self.doc2.id, "Document 2")
        self.graph.add_statement(self.doc2.id, self.type_prop.id, "document")
        self.graph.add_statement(self.doc2.id, self.name_prop.id, "Meeting Notes")
        print("Created Document 2: 'Meeting Notes'")
        
        # Create test tags
        print("\nCreating test tags...")
        self.tag1 = self.graph.create_entity()
        self.graph.add_label(self.tag1.id, "project-alpha")
        self.graph.add_statement(self.tag1.id, self.type_prop.id, "tag")
        
        self.tag2 = self.graph.create_entity()
        self.graph.add_label(self.tag2.id, "meeting")
        self.graph.add_statement(self.tag2.id, self.type_prop.id, "tag")
        print("Created tags: 'project-alpha', 'meeting'")
        
        # Connect documents with tags
        print("\nConnecting documents to their tags...")
        self.graph.add_statement(self.doc1.id, self.tag_prop.id, self.tag1.id)
        self.graph.add_statement(self.doc2.id, self.tag_prop.id, self.tag2.id)
        print("Document 1 tagged with 'project-alpha'")
        print("Document 2 tagged with 'meeting'")

    def test_basic_entity_query(self):
        """Tests querying for entities with basic filtering."""
        print("\n=== Testing Basic Entity Query ===")
        print("Attempting to retrieve Document 1 using its ID...")
        
        result = self.graph.query()\
            .starting_from(self.doc1.id)\
            .return_entities()\
            .execute()
        
        print(f"Query returned {len(result.results)} entity")
        print(f"Entity label: {self.graph.get_latest_label(result.results[0].id)}")
        print(f"Query execution time: {result.execution_time_ms:.2f}ms")
        
        self.assertEqual(len(result.results), 1)
        self.assertEqual(result.results[0].id, self.doc1.id)
        print("✓ Test passed: Successfully retrieved the correct entity")

    def test_follow_relationship(self):
        """Tests following relationships between entities."""
        print("\n=== Testing Relationship Following ===")
        print("Finding all tags associated with Document 1...")
        
        result = self.graph.query()\
            .starting_from(self.doc1.id)\
            .follow(self.tag_prop.id)\
            .return_entities()\
            .execute()
        
        print(f"Query returned {len(result.results)} tag")
        print(f"Tag found: {self.graph.get_latest_label(result.results[0].id)}")
        print(f"Query execution time: {result.execution_time_ms:.2f}ms")
        
        self.assertEqual(len(result.results), 1)
        self.assertEqual(
            self.graph.get_latest_label(result.results[0].id),
            "project-alpha"
        )
        print("✓ Test passed: Successfully followed relationship to find correct tag")

    def test_filter_results(self):
        """Tests filtering query results."""
        print("\n=== Testing Result Filtering ===")
        print("Finding all entities of type 'document' from a mixed set of entities...")
        
        def is_document(entity):
            for statement in self.graph.statements:
                if (statement.subject == entity.id and 
                    statement.predicate == self.type_prop.id and 
                    statement.object == "document"):
                    return True
            return False
        
        result = self.graph.query()\
            .starting_from([self.doc1.id, self.doc2.id, self.tag1.id])\
            .filter(is_document)\
            .return_entities()\
            .execute()
        
        print(f"Query returned {len(result.results)} documents")
        print("Documents found:")
        for entity in result.results:
            print(f"- {self.graph.get_latest_label(entity.id)}")
        print(f"Query execution time: {result.execution_time_ms:.2f}ms")
        
        self.assertEqual(len(result.results), 2)
        result_labels = {self.graph.get_latest_label(e.id) for e in result.results}
        self.assertEqual(result_labels, {"Document 1", "Document 2"})
        print("✓ Test passed: Successfully filtered and found all documents")

    def test_query_metadata(self):
        """Tests that query results include proper metadata."""
        print("\n=== Testing Query Metadata ===")
        print("Executing a query and checking its metadata...")
        
        result = self.graph.query()\
            .starting_from([self.doc1.id, self.doc2.id])\
            .return_entities()\
            .execute()
        
        print(f"Total matches found: {result.total_matches}")
        print(f"Query execution time: {result.execution_time_ms:.2f}ms")
        
        self.assertIsInstance(result, QueryResult)
        self.assertEqual(result.total_matches, 2)
        self.assertGreater(result.execution_time_ms, 0)
        print("✓ Test passed: Query returned proper metadata")

if __name__ == '__main__':
    print("\n=== Graph Query System Tests ===")
    print("Testing our graph query system with a document management scenario")
    print("This test suite will verify basic querying, relationship traversal,")
    print("filtering, and metadata reporting capabilities.")
    print("=" * 50)
    unittest.main(verbosity=1)
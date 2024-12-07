# 6. Interfaces and APIs

## 6.1 Application Developer Interface

The Application Developer Interface (ADI) provides a familiar and intuitive way for developers to interact with the system. Rather than requiring developers to understand graph structures or storage mechanisms, the ADI allows them to work with data structures that match their application's needs.

When an application developer wants to integrate with Yggra, they begin by declaring their data requirements through a schema definition. For example, a contact management application might define its needs like this:

```python
class ContactSchema:
    def __init__(self):
        # Define the structure needed by the application
        self.structure = {
            "table_name": "contacts",
            "fields": {
                "full_name": {"type": "text", "required": True},
                "email": {"type": "text", "format": "email"},
                "phone_numbers": {"type": "array", "items": {"type": "text"}},
                "addresses": {"type": "array", "items": {"type": "object"}},
                "groups": {"type": "array", "items": {"type": "text"}},
                "notes": {"type": "text", "required": False}
            },
            "indexes": ["full_name", "email"],
            "access_pattern": "read_heavy"
        }
```

The system then provides the application with its preferred data interface. For a traditional application expecting SQL access, the system might provide:

```python
class ContactManager:
    def __init__(self, schema: ContactSchema):
        # System creates and manages the database
        self.db = SQLiteInterface(schema)
        
    def query_contacts(self, filters: dict) -> List[Contact]:
        # Developer uses familiar SQL patterns
        return self.db.query("SELECT * FROM contacts WHERE ?", filters)
        
    def add_contact(self, contact: Contact):
        # Changes are automatically synchronized with graph
        self.db.insert("contacts", contact.to_dict())
        
    def update_contact(self, contact_id: str, updates: dict):
        # Updates propagate through the system
        self.db.update("contacts", contact_id, updates)
```

## 6.2 Storage Backend Interface

The Storage Backend Interface (SBI) enables the integration of different storage systems while maintaining consistent behavior and guarantees. This interface allows the system to optimize storage placement without affecting other components.

A storage backend must implement the following core interface:

```python
class StorageBackend:
    def store(self, data: bytes, metadata: dict) -> StorageReference:
        """Store data and return a reference for future retrieval.
        
        The metadata dictionary includes:
        - content_type: MIME type of the content
        - size: Size in bytes
        - hash: Content hash for verification
        - access_pattern: Expected usage pattern
        - sensitivity: Data sensitivity level
        """
        pass
    
    def retrieve(self, reference: StorageReference) -> bytes:
        """Retrieve data using its storage reference.
        
        The system handles caching and access control before calling this method.
        The implementation should focus on efficient data retrieval.
        """
        pass
    
    def verify(self, reference: StorageReference) -> bool:
        """Verify that stored data matches its reference."""
        pass
    
    def delete(self, reference: StorageReference):
        """Remove data from storage.
        
        This is called only after the system ensures no valid references exist.
        """
        pass
```

## 6.3 Query Interface

The Query Interface provides a way to search and analyze data across the graph while maintaining privacy boundaries and access controls. This interface supports both simple lookups and complex graph traversals.

The query interface uses a fluent API design for readability and composability:

```python
class GraphQuery:
    def starting_from(self, entity_type: str) -> 'GraphQuery':
        """Begin query from entities of a specific type."""
        pass
    
    def following(self, relationship: str) -> 'GraphQuery':
        """Follow relationships between entities."""
        pass
    
    def where(self, conditions: dict) -> 'GraphQuery':
        """Filter results based on property values."""
        pass
    
    def select(self, properties: List[str]) -> 'GraphQuery':
        """Specify which properties to return."""
        pass
    
    def execute(self) -> QueryResult:
        """Execute the query and return results."""
        pass

# Example usage
results = graph.query()\
    .starting_from("Contact")\
    .following("member_of")\
    .where({"group_name": "Family"})\
    .select(["full_name", "phone"])\
    .execute()
```

## 6.4 Sharing Interface

The Sharing Interface enables controlled data sharing between users while maintaining privacy and security. This interface allows applications to create and manage secure views of personal data.

```python
class SharingManager:
    def create_share(self, data_selector: dict, 
                    recipient: str,
                    permissions: dict,
                    expiration: datetime) -> ShareToken:
        """Create a secure share of selected data.
        
        The data_selector defines what to share
        permissions specify allowed operations
        expiration sets when access should end
        """
        pass
    
    def accept_share(self, token: ShareToken) -> SharedView:
        """Accept and initialize access to shared data."""
        pass
    
    def revoke_share(self, token: ShareToken):
        """Immediately revoke access to shared data."""
        pass
    
    def list_active_shares(self) -> List[ShareInfo]:
        """List all active outgoing shares."""
        pass
```

Each interface includes comprehensive error handling, logging, and monitoring capabilities. The interfaces are designed to be:
- Intuitive for developers familiar with similar systems
- Safe by default, preventing common security mistakes
- Efficient for common operations
- Flexible enough to support advanced use cases
- Self-documenting through clear method names and parameters

The combination of these interfaces enables developers to build sophisticated applications while leveraging the full power of the personal graph system, all without needing to understand the internal complexity of the implementation.



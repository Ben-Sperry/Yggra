# 9. Examples and Use Cases

## 9.1 Social Media Application

Let's examine how Yggra transforms the traditional social media experience by putting users in control of their data while enabling rich social interactions. Consider a decentralized social media application called "Connections."

When a user first launches Connections, instead of creating a new database, the application registers its data requirements with Yggra:

```python
class ConnectionsSchema:
    def __init__(self):
        self.content_types = {
            "Post": {
                "required": ["content", "timestamp", "author"],
                "optional": ["location", "mood", "attachments"],
                "relationships": ["comments", "reactions", "mentions"]
            },
            "Profile": {
                "required": ["display_name", "avatar"],
                "optional": ["bio", "interests", "location"],
                "relationships": ["follows", "blocks"]
            }
        }
```

The system then creates appropriate views by mapping these requirements to existing personal data. For instance, the Profile might reuse contact information already in the user's graph, while ensuring privacy through careful property mapping.

When the user creates a post, rather than sending it to a central server, the content becomes part of their personal graph:

```python
class Post:
    def create(self, content, attachments=None):
        # Store content in user's graph
        post_entity = graph.create_entity("Post")
        graph.add_statement(post_entity, "content", content)
        
        # Handle attachments through storage layer
        if attachments:
            for attachment in attachments:
                ref = storage.store(attachment.data)
                graph.add_statement(post_entity, "has_attachment", ref)
        
        # Create sharing view for followers
        share = sharing.create_view(post_entity, "followers")
        return share.public_url
```

What makes this approach powerful is how it enables new kinds of social interactions. For example, when someone comments on a post, their comment lives in their own graph but creates a relationship to the original post. This means users maintain ownership of their contributions while preserving the conversational context.

## 9.2 Personal Information Management

Consider a personal information management system that helps users organize their lives across multiple domains. Instead of creating separate databases for different types of information, the system leverages Yggra's unified graph structure.

A task management application might interact with calendar events, contacts, and documents through a unified view:

```python
class PersonalOrganizerView:
    def create_task(self, task_data):
        # Create task entity
        task = graph.create_entity("Task")
        graph.add_statements([
            (task, "title", task_data.title),
            (task, "due_date", task_data.due_date)
        ])
        
        # Link to relevant entities
        if task_data.related_contact:
            contact = graph.find_entity("Contact", task_data.related_contact)
            graph.add_statement(task, "involves_person", contact)
            
        if task_data.related_document:
            doc = graph.find_entity("Document", task_data.related_document)
            graph.add_statement(task, "references", doc)
            
        return task

    def get_context(self, entity_id):
        # Retrieve rich context for any entity
        return graph.query()
            .starting_from(entity_id)
            .follow_relationships(["involves_person", "references"])
            .include_reverse_relationships()
            .execute()
```

This approach enables powerful features like automatic context gathering. When viewing a task, the system can show relevant emails, calendar events, and documents, all connected through the graph structure.

## 9.3 Content Sharing

The content sharing use case demonstrates how Yggra handles both personal content management and controlled sharing. Consider a photo management application that allows users to organize and share their photos while maintaining complete control over their content.

When a user imports photos, the system processes them intelligently:

```python
class PhotoManager:
    def import_photos(self, photo_files):
        for photo in photo_files:
            # Store photo data
            photo_data = storage.analyze(photo)
            storage_ref = storage.store(
                photo.data,
                content_type="image",
                metadata=photo_data.metadata
            )
            
            # Create photo entity
            photo_entity = graph.create_entity("Photo")
            
            # Add basic metadata
            graph.add_statements([
                (photo_entity, "storage_ref", storage_ref),
                (photo_entity, "taken_date", photo_data.date),
                (photo_entity, "camera", photo_data.camera)
            ])
            
            # Add location if available
            if photo_data.location:
                location = graph.create_or_find_entity(
                    "Location",
                    photo_data.location
                )
                graph.add_statement(photo_entity, "taken_at", location)
            
            # Detect and link to people
            for face in photo_data.detect_faces():
                person = graph.find_similar_entity("Person", face)
                if person:
                    graph.add_statement(photo_entity, "shows_person", person)
```

When sharing photos, users can create sophisticated sharing rules:

```python
class PhotoSharing:
    def create_album_share(self, photos, recipients, privacy_rules):
        view = sharing.create_view({
            "entities": photos,
            "properties": {
                "include": ["image", "taken_date", "location"],
                "exclude": ["camera_settings", "original_file"]
            },
            "transformations": {
                "location": "city_level_only",
                "image": "watermark"
            },
            "duration": "30_days"
        })
        
        return view.share(recipients)
```

## 9.4 Data Analysis

The data analysis use case shows how Yggra enables personal analytics while maintaining privacy. Users can analyze their data across different applications while maintaining complete control over what insights are shared.

A personal analytics application might track health data across multiple sources:

```python
class HealthAnalytics:
    def analyze_health_trends(self, date_range):
        # Gather data from various sources
        health_data = graph.query()
            .find_type("HealthMetric")
            .in_time_range(date_range)
            .include_related("Activity", "Sleep", "Nutrition")
            .execute()
            
        # Perform analysis while maintaining privacy
        insights = analyze_private(health_data)
        
        # Create shareable summary
        summary_view = sharing.create_view({
            "data": insights,
            "level": "aggregate_only",
            "minimum_group_size": 10
        })
        
        return summary_view
```

This enables users to gain insights from their data while maintaining granular control over what information is shared with healthcare providers or research studies.
# Salestack Tech Challenge (to-do app)

This project is a ScalesStack Tech Challenge for applying Python Developer position. It has been developed in Django Framework as requested.

## Excercise

The candidate should set up a Django project and create a new app called "todo."
Create a model for a To-Do list with fields such as "title" and "description"
Create a model for a To-Do list item with fields such as "title", "description", "created_at"
and "completed" (a boolean).
Expose RESTful API endpoints for the following operations:
- Create a new To-Do list.
- Add a new To-Do item to a list.
- Retrieve all To-Do items from a list.
- Retrieve details of a specific To-Do item.
- Update the status (completed/uncompleted) of a To-Do item.
- Delete a To-Do item.
- Use Django's ORM to perform database operations.

## Solution

The solution is expressed in this repo in [github](https://github.com/IgnacioAramburu/todo-app). The repo is public and you can easily access and clone it in your computer as any other github project by this  command in your bash:

```
  git clone https://github.com/IgnacioAramburu/todo-app.git
```

**NOTE**: For making the evaluation much easier, I uploaded the project already containerized in Google Cloud Platform (GCP) to run in serverless environment with full and public internet access, so you don't have to run it internally in your computer. 
It will stay there until the end of this stage of the process, so please let me know when the stage is completed.
The API URL is https://tech-challenge-ol2daf64nq-uc.a.run.app

### Some considerations
- The Project uses **Django Web Framework** 5.0.2 and **Django Rest Framework** 3.14 in its structure. The last one provides serializer capabilities between ORM Model and View logic, which helps managing the data Django ORM instances and querysets in Python data types, that later can be easily convert in JSON data types.
- The Project uses Django ORM for the Database Mapping and to perform all DB Operations.
- Unit testing is not included in the scope of this excercise.
- The Database is a SQLite serverless database containerized in the same container as the Project for simplification. 
- The project name may be seen in the repo as _tech_challenge_ meanwhile the to-do app API name may be seen as _todo-api_.

### ORM Model Design (performed with Django ORM as requested)

```
class ToDoList(models.Model):
    title = models.CharField(null=False, blank=False, max_length=50) #requested by exercise
    description = models.CharField(null=False, default="", max_length=200) #requested by exercise
    completed = models.BooleanField(default=True) #requested by exercise: It updates to false if any item in the list has 'completed' field as False.
    size = models.IntegerField(default=0) #extra: for checking amount of items in the list, it updates according the number of related items in the list.
    created_at = models.DateField(default=date.today) #extra: for checking creation date.
    last_updated_at = models.DateField(default=date.today) #extra: for checking last_updated date.

class ToDoItem(models.Model):
    title = models.CharField(null=False, blank=False, max_length=50) #requested by exercise
    description = models.CharField(null=False, default="", max_length=400) #requested by exercise
    completed = models.BooleanField(default=False) #requested by exercise.
    created_at = models.DateField(default=date.today) #extra: for checking creation date.
    last_updated_at = models.DateField(default=date.today) #extra: for checking last_updated date.
    list = models.ForeignKey(ToDoList, on_delete=models.CASCADE) #ToDoList <- 1:n -> ToDoItem relationship
```

### About the requested endpoints:

---

#### Endpoint 1: Create a new To-Do list.

This endpoint is used to create a To-Do list instance in DB. The how-to use it is shown below:

```
HTTP_METHOD = POST
URL = https://tech-challenge-ol2daf64nq-uc.a.run.app/api/lists
BODY = {
    "title":"Any Title",
    "description":"Any Description",
}
```

- If _title_ not provided, the request will produce an error, because field value is mandatory.
- _description_ is not mandatory field, but default it takes empty string value

---

#### Endpoint 2: Add a new To-Do item to a list.

This endpoint is used to create a To-Do item instance and associate it to a To-Do list instance in the DB. The how-to use it is shown below:

```
HTTP_METHOD = POST
URL = https://tech-challenge-ol2daf64nq-uc.a.run.app/api/items/list/<int:list_id>
BODY = {
    "title":"Any Title",
    "description":"Any Description",
    "completed":true
}
```

- list_id is a path parameter and must be replaced by the integer number representing list_id where the new item will be associated.
- If _title_ not provided, the request will produce an error, because field value is mandatory.
- _description_ and _completed_ are not mandatory fields. Their default value is empty string and false respectively
- Adding a new list item to a list will perform an update in the value of the related ToDo List instance 'size' field adding +1 to the current value, to represent that the list has a new item so, its size (amount of items) has increased
- Adding a new list item will force in a the value of the related ToDo List instance 'completed' field to false if the added item has its 'completed' field as false.

---

#### Endpoint 3: Retrieve all To-Do items from a list.

There are 2 endpoint to perform this (both retrieves all ToDo items details):

- Endpoint 3.a (By dedicated item endpoint)**: It retrieves all To-Do items instances belonging to the specific ToDo list instance in the DB. The how-to use it is shown below:

  ```
  HTTP_METHOD = GET
  URL = https://tech-challenge-ol2daf64nq-uc.a.run.app/api/items/list/<int:list_id>
  ```
  
  - list_id is a path parameter and must be replaced by the integer number representing list_id of the list which items you are looking for.

- Endpoint 3.b (By extended list endpoint)**: It retrieves, apart from all list details, all To-Do items belonging to the specific To-Do list instance in the DB, only if the query string parameter 'include_items' is included and set with 'true' value. The how-to use it is shown below:
  
  ```
  HTTP_METHOD = GET
  URL = https://tech-challenge-ol2daf64nq-uc.a.run.app/api/lists/<int:list_id>?include_items=true
  ```
  
  - 'list_id' is a path parameter and must be replaced by the integer number representing list_id of the list which items you are looking for.
  - 'include_items' is a query string parameter that must be added and set with 'true' value to allow all the related To-Do items to be retrieved with the list information as well.
  - In the response body, the To-Do items are brought by the 'todoitem_set' field. It's a list with all items details that are related with the given To-Do list id.

---

#### Endpoint 4: Update the status (completed/uncompleted) of a To-Do item.

This endpoint is used to update a To-Do item instance information in any of its fields in the DB. For changing  the completed/uncompleted value of the To-Do item, will only have to update the 'completed' boolean field in the To-Do item instance with the desired boolean value (true for completed, false for uncompleted). The how-to use it is shown below:

```
HTTP_METHOD = PUT
URL = https://tech-challenge-ol2daf64nq-uc.a.run.app/api/items/<int:item_id>
BODY = {
    "completed":true
}
```

- item_id is a path parameter and must be replaced by the integer number representing item_id which 'completed' field must be updated.
- When modifying 'completed' field value, the related to-do-list Field instance field 'completed' will also be updated to false if the To-Do item was updated with false value.

---

#### Endpoint 5: Delete a To-Do item..

This endpoint is used for deleting the To-Do item by its given id. The how-to use it is shown below:

```
HTTP_METHOD = DELETE
URL = https://tech-challenge-ol2daf64nq-uc.a.run.app/api/item/<int:item_id>
```

- item_id is a path parameter and must be replaced by the integer number representing item_id which 'completed' field must be deleted.
- When deleting the a To-Do item, the related list 'size' field is decrease by one, to indicate the amount of items related to list was decreased by the deleted item.
- When deleting the a To-Do item, the related list 'completed' field is updated to 'true' if no more To-Do items related to the list has their 'completed' as 'false', else the completed field is updated to 'false'.

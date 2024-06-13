import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import ToDo as ToDoModel, db

class ToDoType(SQLAlchemyObjectType):
    class Meta:
        model = ToDoModel

class Query(graphene.ObjectType):
    all_todos = graphene.List(ToDoType)

    def resolve_all_todos(self, info):
        query = ToDoType.get_query(info)
        return query.all()

class CreateToDo(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        time = graphene.DateTime(required=True)
        image = graphene.String()

    todo = graphene.Field(lambda: ToDoType)

    def mutate(self, info, title, description, time, image=None):
        todo = ToDoModel(title=title, description=description, time=time, image=image)
        db.session.add(todo)
        db.session.commit()
        return CreateToDo(todo=todo)

class Mutation(graphene.ObjectType):
    create_todo = CreateToDo.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

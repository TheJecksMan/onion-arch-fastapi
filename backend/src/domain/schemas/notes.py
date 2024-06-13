from pydantic import BaseModel


class IDModel(BaseModel):
    id: int


class Category(BaseModel):
    title: str


class CategoryWithID(Category, IDModel):
    pass


class CreateNote(BaseModel):
    title: str
    text: str

    categories: list[int]


class EditNote(IDModel):
    title: str
    text: str

    categories: list[int]


class NoteWithID(IDModel):
    title: str
    text: str

    categories: list[CategoryWithID]

from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base


class Categories(Base):
    """
     Represents a category for notes.

    Attributes:
        id (`int`): The unique identifier for the category.
        title (`str`): The title of the category. Must be unique and not nullable.
        notes (`list[Notes]`): The list of notes associated with this category.
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    notes: Mapped[list["Notes"]] = relationship(
        secondary="notes_categories", back_populates="categories"
    )

    def __repr__(self):
        return f"<Categories(id={self.id}, title={self.title})>"


class Notes(Base):
    """
    Represents a note.

    Attributes:
        id (`int`): The unique identifier for the note.
        title (`str`): The title of the note. Not nullable.
        text (`str`): The text content of the note.
        categories (`list[Categories]`): The list of categories associated with this note.
    """

    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(400), nullable=False)
    text: Mapped[str] = mapped_column(Text)

    categories: Mapped[list["Categories"]] = relationship(
        secondary="notes_categories", back_populates="notes"
    )

    def __repr__(self):
        return f"<Notes(id={self.id}, title={self.title}, text={self.text[:15]})>"


class CategoriesNotes(Base):
    __tablename__ = "notes_categories"

    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), primary_key=True)

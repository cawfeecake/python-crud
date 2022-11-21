import json
from typing import List, Type


from sqlalchemy.sql import func


from .database import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

    children = db.Column(db.String, nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    update_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


    # TODO make these wrappers for a setter
    def add_child(self, child):
        children_obj = json.loads(self.children) if self.children else []
        if child not in children_obj:
            children_obj.append(child)
            self.children = json.dumps(children_obj)

    def remove_child(self, child):
        children_obj = json.loads(self.children)
        children_obj.remove(child)
        self.children = '' if len(children_obj) == 0 else json.dumps(children_obj)


    def __repr__(self):
        return f'<Item({self.id}) {{ name="{self.name}", description="{self.description}", num_of_children="{len(json.loads(self.children))}" }}>'

    def __str__(self):
        json_str = {
          "id": self.id,
          "name": self.name,
          "description": self.description,
          "child_items": f"[{ ', '.join(json.loads(self.children)) }]",
          "created_at": self.created_at,
          "update_at": self.update_at,
        }
        return json.dumps(json_str, indent=4, default=str)


def add_item(name: str, desc: str, children: List[str]) -> Type[Item]:
        new_item = Item(name=name, description=desc)
        for c in children:
            new_item.add_child(c)

        db.session.add(new_item)
        db.session.commit()
        return new_item

def delete_item(item: Item) -> None:
        db.session.delete(item)
        db.session.commit()

def update_item(item: Item, name: str, desc: str, children: List[str]) -> Type[Item]:
        item.name = name
        item.description = desc
        for c in children:
            item.add_child(c)

        db.session.commit()
        return item

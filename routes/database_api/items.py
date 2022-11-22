import json

from sqlalchemy.sql import func

from .database import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

    children = db.Column(db.String)

    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    update_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'children':
                json.loads(self.children) if self.children else [],
            'created_at': self.created_at,
            'update_at': self.update_at,
        }

    def add_child(self, child):
        children_obj = json.loads(self.children) if self.children else []
        if child not in children_obj:
            children_obj.append(child)
            self.children = json.dumps(children_obj)

    def remove_child(self, child):
        children_obj = json.loads(self.children) if self.children else []
        if children_obj:
            children_obj.remove(child)
            self.children = json.dumps(children_obj)

    def __repr__(self):
        obj = self.to_json()
        return f'<Item({obj["id"]}) {{ name="{obj["name"]}", description="{obj["description"]}", num_of_children="{len(obj["children"])}" }}>'

    def __str__(self):
        obj = self.to_json()
        return json.dumps(obj, indent=2, default=str)
        # dev: `default=str` is to convert nonserialize by calling str() which
        #      is useful for displaying the datetime objects


def add_item(name: str, desc: str, children: list[str]) -> Item:
        new_item = Item(name=name, description=desc)
        for c in children:
            new_item.add_child(c)

        db.session.add(new_item)
        db.session.commit()
        return new_item

def delete_item(item: Item) -> None:
        db.session.delete(item)
        db.session.commit()

def update_item(item: Item, name: str, desc: str, children: list[str]) -> Item:
        item.name = name
        item.description = desc
        for c in children:
            item.add_child(c)

        db.session.commit()
        return item

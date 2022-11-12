import json


from flask import current_app as app, redirect, request, url_for
from markupsafe import escape
from sqlalchemy.sql import func


from backend import db
#db = current_app.extensions['sqlalchemy'].db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

    children = db.Column(db.String, nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    update_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


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


# data = [
#     ('name', 'desc', children) ...,
#     ('comb', 'used to brush my hair', []),
#     ('cabinet', '3 stacked plastic drawers', [-1]),
# ]
@app.route('/items/', methods=['GET', 'POST'])
def get_items():
    insert_ids = None
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')

        new_item = Item(name=name, description=desc)

        for child in request.form.get('children').split():
            new_item.add_child(child)

        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('get_items'))

    all_items = Item.query.all()
    inserted_str = ''
    #{ f'<p>Created: { " ".join([str(i) for i in insert_ids]) }</p>' if insert_ids else '' }
    return f"""
        <a href="{ url_for('index') }">&lt; Back</a>
        <form method="POST">
          <div><label>Name: <input type="text" name="name"></label></div>
          <div><label>Description: <input type="text" name="desc"></label></div>
          <div><label>Children: <input type="text" name="children"></label></div>
          <input type="submit" value="Create">
        </form>
        <hr />
        { f'<p>{inserted_str}</p>' if inserted_str else '' }
        <p>Count: { len(all_items) }</p>
        <ul>
        { ''.join([ f'<li><a href="{ url_for("get_item_by_id", item_id=i.id) }">{ escape(repr(i)) }</a></li>' for i in all_items ]) }
        </ul>
    """


@app.route('/items/<int:item_id>/', methods=['GET', 'DELETE', 'POST'])
def get_item_by_id(item_id):
    retr_item = Item.query.get_or_404(item_id)
    if request.method == 'DELETE':
        db.session.delete(retr_item)
        db.session.commit()
        return redirect(url_for('get_items'))
    elif request.method == 'POST':
        retr_item.name = request.form.get('name')
        retr_item.description = request.form.get('desc')
        for child in request.form.get('children').split():
            retr_item.add_child(child)
        db.session.commit()
        return redirect(url_for('get_item_by_id', item_id=item_id)) # can modify client to save on server req.
    return f"""
        <a href="{ url_for('get_items') }">&lt; Back</a>
        <p>{ escape(str(retr_item)) }</p>
        <hr />
        <form method="POST">
          <div><label>Name: <input type="text" name="name"></label></div>
          <div><label>Description: <input type="text" name="desc"></label></div>
          <div><label>Children to add: <input type="text" name="children"></label></div>
          <input type="submit" value="Update">
        </form>
        <button onclick="delete_item()">Delete</button>
        <script>
          function delete_item() {{
            const delete_url = '{ url_for('get_item_by_id', item_id=item_id) }';
            fetch(delete_url, {{ method: 'DELETE' }})
              .then(() => {{ window.location.href = '{ url_for('get_items') }'; }});
          }}
        </script>
    """

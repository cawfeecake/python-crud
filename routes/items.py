from flask import current_app as app, redirect, request, url_for


from databases.items import *


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
        child = request.form.get('child')
        insert_ids = items.insert_data([(name, desc, Children([child, 1]))])
        return redirect(url_for('get_items'))
    all_items = items.get_all()
    return f"""
        <a href="{ url_for('index') }">&lt; Back</a>
        <form method="POST">
          <div><label>Name: <input type="text" name="name"></label></div>
          <div><label>Description: <input type="text" name="desc"></label></div>
          <div><label>A child: <input type="text" name="child"></label></div>
          <input type="submit" value="Submit">
        </form>
        <hr />
        { f'<p>Inserted: { " ".join([str(i) for i in insert_ids]) }</p>' if insert_ids else '' }
        <p>Count: {len(all_items)}</p>
        <p>{all_items}</p>
    """


@app.route('/items/<int:item_id>/', methods=['GET', 'DELETE', 'POST'])
def get_item_by_id(item_id):
    if request.method == 'DELETE':
        items.delete_by_id(item_id)
        return 'OK', 204
    elif request.method == 'POST':
        movie_name = request.form.get('name')
        movie_year = request.form.get('year')
        rating_x, rating_y = (float(request.form.get('x')), float(request.form.get('y')))
        update_data = [movie_name, movie_year, Point(rating_x, rating_y)]
        items.update_by_id(item_id, update_data)
        return redirect(url_for('get_item_by_id', item_id=item_id))
    return f"""
        <a href="{ url_for('get_items') }">&lt; Back</a>
        <p>{items.get_by_id(item_id)}</p>
        <hr />
        <form method="POST">
          <div><label>Name: <input type="text" name="name"></label></div>
          <div><label>Year: <input type="text" name="year"></label></div>
          <div><label>Rating Point: <input type="text" name="x"><input type="text" name="y"></label></div>
          <input type="submit" value="Update">
        </form>
    """

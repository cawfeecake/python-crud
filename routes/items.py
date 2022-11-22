from flask import current_app as app, jsonify, redirect, render_template, request, url_for


from .database_api.items import Item, add_item, delete_item, update_item


@app.route('/items/', methods=['GET', 'POST'])
def get_items():
    if request.method == 'POST':
        if request.is_json:
            req_data = request.json
        else:
            req_data = request.form

        name = req_data.get('name')
        desc = req_data.get('desc')
        children = req_data.get('children').split()

        new_item = add_item(name, desc, children)
        app.logger.info(f'new item was successfully created ({new_item.id})')

        # uncomment to redirect to newly created item
        #return redirect(url_for('get_item_by_id', item_id=new_item.id))

    all_items = Item.query.all()
    if request.accept_mimetypes.accept_html:
        return render_template('items.html', items=all_items)
    return jsonify([ elem.to_json() for elem in all_items ])

@app.route('/items/<int:item_id>/', methods=['GET', 'DELETE', 'POST'])
def get_item_by_id(item_id):
    retr_item = Item.query.get_or_404(item_id)
    if request.method == 'DELETE':
        delete_item(retr_item)
        return redirect(url_for('get_items'))
    elif request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        children = request.form.get('children').split()

        update_item(retr_item, name, desc, children)

    if request.accept_mimetypes.accept_html:
        return render_template('item.html', item=retr_item)
    return jsonify(retr_item.to_json())

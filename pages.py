from flask import Blueprint, render_template, request, session, flash, redirect, jsonify
import db

DOMAIN = 'http://127.0.0.1:5000'

active_sessions = {}

pages = Blueprint('pages', __name__, static_folder='static', template_folder='template')

def create_route(wrapped_name, route, file_name, recipe_name):
    """
    A function that returns a route to a website endpoint
    The function creates a route for endpoints with the same logic
    """
    def wrapped():
        if request.method == 'GET':
            if 'session_id' in session and session['session_id'] in active_sessions:
                return render_template(file_name, domain=DOMAIN, user=active_sessions[session['session_id']], recipe_name=recipe_name)
            else:
                return render_template(file_name, domain=DOMAIN, user=None)
        else:
            if 'session_id' in session and session['session_id'] in active_sessions:
                # Pull json data from ajax request and set new rating
                user = active_sessions[session['session_id']]
                json_data = request.get_json()
                new_rating = json_data.get('recipe_rate')
                # Explicit check because new rating may be equal to 0
                if new_rating is not None:
                    result = db.update_user(user.email, 'rating', (recipe_name, new_rating))
                    if result == 1:
                        # Update data in active sessions and return 200 status code response
                        active_sessions[session['session_id']].ratings[recipe_name] = new_rating
                        return jsonify(success=True), 200
                    else:
                        return jsonify(success=False), 400
                else:
                    return jsonify(success=False), 400
                
            else:
                return jsonify(success=False), 403
    wrapped.__name__ = wrapped_name
    # Returns new route to endpoint
    pages.route(route, methods=['GET', 'POST'])(wrapped)

# Create route for each of the website pages
create_route('cake','/cake', 'cake.html', 'Cake')
create_route('brownies', '/brownies', 'brownies.html', 'Brownies')
create_route('hot_chocolate', '/hot-chocolate', 'hotcho.html', 'Hot Chocolate')
create_route('chocolate_pudding', '/chocolate-pudding', 'chopud.html', 'Chocolate Pudding')
create_route('molten_cake', '/molten-cake', 'molcho.html', 'Molten Cake')
create_route('molten_chocolate_cake','/molten-chocolate-cake', 'molcho.html', 'Molten Cake')
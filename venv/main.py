from flask import Flask, make_response, jsonify, request;
from repositorie import Projects;

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/api', methods=["GET"])
def get_projects():
    return make_response(
        jsonify(
            message="Projects",
            data=Projects
        ), 201
    )
    

@app.route('/api/project/<int:id>', methods=["GET"])
def get_project(id):
    try:
        index = find_by_id(id)
        
        return make_response(
            jsonify(
                message="Projects",
                data=Projects[index]
            ), 201
        )
    except: 
        return make_response(jsonify({"error": "Project not found"}), 404) 
   

@app.route('/api/project', methods=["POST"])
def add_project():
    project = request.json
    Projects.append(project)
    
    return make_response(
        jsonify(
            message="Projects",
            data=project
        ), 201
    )


@app.route('/api/project/<int:id>', methods=["PUT"])
def edit_project(id):
    project_new_data = request.json
    try:
        index = find_by_id(id)
        Projects[index] = project_new_data
        
        return make_response(jsonify(Projects[index]), 201)
    except: 
        return make_response(jsonify({"error": "Project not found"}), 404) 


@app.route('/api/project/<int:id>', methods=["DELETE"])
def delete_project(id):
    try:
        index = find_by_id(id)
        Projects.remove(Projects[index])
        
        return make_response(jsonify({"success": "Your project has been deleted"}), 201)
    except:
        return make_response(jsonify({"error": "Has occurred an error for delete this project"}), 404)
    

@app.route('/api/project/expenses/<int:id>', methods=["GET"])
def get_expenses(id):
    try:
        index = find_by_id(id)
         
        return make_response(jsonify(Projects[index]["expenses"]), 201)
    except:
        return make_response(jsonify({"error": "Has occurred an error for show this expenses"}, 404))
    
    
@app.route('/api/project/expenses/<int:id>/<int:expense_id>', methods=["GET"])
def get_expense(id, expense_id):
    try:
        index = find_by_id(id)
        try:
            expense_index = find_expense(Projects[index]["expenses"], expense_id)
            print(expense_index)
                
            expense = Projects[index]["expenses"][expense_index]
            return make_response(jsonify(expense), 201)
        except:    
            return make_response(jsonify({"error": "Has occurred an error for show this expense."}), 404)     
    except:
        return make_response(jsonify({"error": "Has occurred an error for show this expense"}), 404)
    

@app.route('/api/project/expenses/<int:id>/<int:expense_id>', methods=["GET"])
def delete_expense(id, expense_id):
    try: 
        index = find_by_id(id)
        try:
            expense = find_expense(Projects[index]["expenses"], expense_id)
            Projects[index]["expenses"].remove(expense)
            
            return make_response(jsonify({"success":"Expense deleted."}, 201))
        except:
            return make_response(jsonify({"error": "Has occurred an error for delete this expense"}, 404)) 
    except:
        return make_response(jsonify({"error": "Has occurred an error for delete this expense"}, 404))
    
 
@app.route('/api/project/expenses/<int:id>/<int:expense_id>', methods=["PUT"])
def edit_expanse(id, expense_id):
    try:
        index = find_by_id(id)
    
        try: 
            expense = find_expense(Projects[index]["expenses"], expense_id)
            Projects[index]["expenses"][expense] = request.json
            
            return make_response(jsonify(Projects[index]["expenses"][expense]), 201)
        except:
            return make_response(jsonify({"error": "Has occurred an error for show this expense"}, 404))    
            
    except:
        return make_response(jsonify({"error": "Has occurred an error for show this expense"}, 404))    


def find_by_id(id):
    for project in Projects:
        if project["id"] == id:
            return int(Projects.index(project))
    
    return len(Projects) + 1


def find_expense(expenses, expense_id):
    for expense in expenses:
        if expense["expense_id"] == expense_id:
            return int(expenses.index(expense))
    
    return len(expenses) + 1


app.run()
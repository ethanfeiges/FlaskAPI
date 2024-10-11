from flask import Flask, request
## timestamp
import datetime
from flask import Flask, request, jsonify, abort
from collections import defaultdict


app = Flask(__name__)

# History of all transactions for a singular user
transactions = []
# Running value of the user's balance
balanceSum = 0
# Dictionary of all balances from each payer.
balances = defaultdict(int)

# Ensures that the data is in the correct format.
def validate_request_data(data):
    payer = data.get('payer')
    points = data.get('points')
    timestamp = data.get('timestamp')
    if not isinstance(points, int):
        abort(400, description="Points must be an integer")
    if payer is not None and not isinstance(payer, str):
        abort(400, description="Payer must be a string if provided")
    if timestamp is not None:
        try:
            timestamp = datetime.datetime.fromisoformat(timestamp)
        except ValueError:
            abort(400, description="Timestamp must be in ISO format if provided")
    
    return payer, points, timestamp

# Handles the addition of points to the user's balance
@app.route('/add', methods=['POST'])
def addPoints():
    global balanceSum
    data = request.get_json()
    payer, points, timestamp = validate_request_data(data)
    if points <= 0:
        ## Check if you are going into a negative balance
        if balances[payer] + points < 0:
            abort(400, description="Cannot go into negative balance")
    # Adds the transaction to the transaction history
    transactions.append([timestamp, payer, points])
    # Adds the points to the running balance
    balances[payer] += points
    balanceSum += points
    return 'Points added!'

# Handles user spending their points 
@app.route('/spend', methods=['POST'])
def spendPoints():
    global balanceSum
    data = request.get_json()
    points = validate_request_data(data)[1]
    # Check if there are enough points to spend.
    if balanceSum < points:
        abort(400, description="Not enough points to spend")
    
    balanceSum -= points
    # Sorts the transactions by timestamp
    transactions.sort(key=lambda x: x[0])
    
    # JSON response in format {"payer": , "points": }
    res = []
    # Deducts the points from the oldest transactions first
    for transaction in transactions:
        if points <= 0:
            break
        # If the points to be deducted exceeds the current transaction
        if points >= transaction[2]:
            points -= transaction[2]
            # Append to response 
            res.append({transaction[1]: -transaction[2]})
            # Update the list of balances
            balances[transaction[1]] -= transaction[2]
            transaction[2] = 0
        # If can be fully deducted from the payer transaction
        else:
            transaction[2] -= points
            # Append to response
            res.append({transaction[1]: -points})
            # Update the list of balances
            balances[transaction[1]] -= points
            points = 0
    return jsonify(res)

# Returns the balance of the user
@app.route('/balance', methods=['GET'])
def getBalance():
    # Returns the balances of each payer as an array of JSON objects
    return jsonify(balances)

if __name__ == '__main__':
    # Runs the app on port 8000
    app.run(port=8000)
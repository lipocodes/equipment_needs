#with open("/home/liorp/silmap/output.txt", "w", encoding="utf-8") as f:
    #f.write(pdf_file.filename + "\n")



import os
import json
from flask import Blueprint, jsonify, request, render_template
import requests

# Blueprint
flask_equipment_needs = Blueprint('flask_equipment_needs', __name__)


JSON_PATH = "/home/liorp/equipment_needs/equipment_list.json"

@flask_equipment_needs.route('/index_equipment_needs', methods=['GET'])
def loadUI():
    return render_template("index_equipment_needs.html")


@flask_equipment_needs.route('/get_equipment', methods=['GET'])
def getEquipment():
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data_json = json.load(f)
        return jsonify(data_json)
    except Exception as e:
        return jsonify({
            "message": "An error occurred",
            "error": str(e)
        }), 500



@flask_equipment_needs.route('/increment_equipment_orders', methods=['POST'])
def incrementEquipmentOrders():
    try:
        data = request.get_json(silent=True)

        if not data or "item" not in data:
            return jsonify({"message": "Missing item"}), 400

        item_name = data["item"]

        # Load JSON
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data_json = json.load(f)

        for equipment in data_json["office_equipment"]:
            if equipment["item"] == item_name:
                equipment["quantity"] = equipment.get("quantity", 0) + 1
                updated_quantity = equipment["quantity"]

                # Save back
                with open(JSON_PATH, "w", encoding="utf-8") as f:
                    json.dump(data_json, f, ensure_ascii=False, indent=2)

                return jsonify({
                    "item": item_name,
                    "quantity": updated_quantity,
                    "status": "ok"
                }), 200

        return jsonify({"message": "Item not found"}), 404

    except Exception as e:
        return jsonify({
            "message": "An error occurred",
            "error": str(e)
        }), 500



@flask_equipment_needs.route('/decrement_equipment_orders', methods=['POST'])
def decrementEquipmentOrders():
    try:
        data = request.get_json(silent=True)

        if not data or "item" not in data:
            return jsonify({"message": "Missing item"}), 400

        item_name = data["item"]

        # Load JSON
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data_json = json.load(f)

        for equipment in data_json["office_equipment"]:
            if equipment["item"] == item_name:
                current_qty = equipment.get("quantity", 0)

                if current_qty <= 0:
                    return jsonify({
                        "item": item_name,
                        "quantity": current_qty,
                        "message": "Quantity already at zero"
                    }), 200

                equipment["quantity"] = current_qty - 1
                updated_quantity = equipment["quantity"]

                # Save back
                with open(JSON_PATH, "w", encoding="utf-8") as f:
                    json.dump(data_json, f, ensure_ascii=False, indent=2)

                return jsonify({
                    "item": item_name,
                    "quantity": updated_quantity,
                    "status": "ok"
                }), 200

        return jsonify({"message": "Item not found"}), 404

    except Exception as e:
        return jsonify({
            "message": "An error occurred",
            "error": str(e)
        }), 500



@flask_equipment_needs.route('/cancel_equipment_orders', methods=['POST'])
def cancelEquipmentOrders():
    try:
        data = request.get_json(silent=True)

        if not data or "item" not in data:
            return jsonify({"message": "Missing item"}), 400

        item_name = data["item"]

        # Load JSON file
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data_json = json.load(f)

        for equipment in data_json["office_equipment"]:
            if equipment["item"] == item_name:
                equipment["quantity"] = 0
                updated_quantity = equipment["quantity"]

                # Save back to JSON
                with open(JSON_PATH, "w", encoding="utf-8") as f:
                    json.dump(data_json, f, ensure_ascii=False, indent=2)

                return jsonify({
                    "item": item_name,
                    "quantity": updated_quantity,
                    "status": "ok"
                }), 200

        # If we get here, item was not found
        return jsonify({"message": "Item not found"}), 404

    except Exception as e:
        return jsonify({
            "message": "An error occurred",
            "error": str(e)
        }), 500



@flask_equipment_needs.route('/add_item', methods=['POST'])
def addItem():
    try:
        data = request.get_json(silent=True)

        # Check if "item" is in the request
        if not data or "item" not in data:
            return jsonify({"message": "Missing item name"}), 400

        new_item_name = data["item"]

        # Read the existing JSON file
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            equipment_data = json.load(f)

        # Optional: prevent duplicates
        for equipment in equipment_data["office_equipment"]:
            if equipment["item"] == new_item_name:
                return jsonify({"message": "Item already exists"}), 400

        # Create the new item object
        new_item = {
            "item": new_item_name,
            "quantity": data.get("quantity", 0)  # default quantity 0
        }

        # Append to the list
        equipment_data["office_equipment"].append(new_item)

        # Save back to the JSON file
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(equipment_data, f, ensure_ascii=False, indent=4)

        return jsonify({"message": "Item added successfully", "item": new_item}), 200

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

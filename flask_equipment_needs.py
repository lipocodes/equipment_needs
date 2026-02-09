#with open("/home/liorp/silmap/output.txt", "w", encoding="utf-8") as f:
    #f.write(pdf_file.filename + "\n")

import os
import json
from flask import Blueprint, jsonify, request, render_template
import requests

# Blueprint
flask_equipment_needs = Blueprint('flask_equipment_needs', __name__)

@flask_equipment_needs.route('/index_equipment_needs', methods=['GET'])
def loadUI():
    return render_template("index_equipment_needs.html")

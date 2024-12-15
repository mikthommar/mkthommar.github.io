from flask import Flask, jsonify, request, render_template
import mongoengine as db
import json

app = Flask(__name__)

client = db.connect('animehub', username='', password='')

supported_regions = [ 'NorthAmerica', 'Europe', 'Asia', 'Caribbean', 'SouthAmerica' ]
supported_regions_delivery_cost = [ 150, 200, 100, 50, 175 ]

pkge_price = [ 400, 800, 1500, 3000, 1000 ]

class Order(db.Document) :
  custName = db.StringField()
  custAddress = db.StringField()
  custRegion = db.StringField()
  custEmail = db.StringField()
  custNo = db.StringField()
  pkgeNo = db.IntField()
  totPrice = db.IntField()
  
  meta = { 'collection' : 'orders', 'allow_inheritance': False }

class Package(db.Document) :
  pckid = db.StringField()
  name = db.StringField()
  desc = db.StringField()
  price = db.StringField()
  
  meta = { 'collection' : 'package', 'allow_inheritance': False }
  


# http://localhost:5000/home
@app.route('/home', methods=['GET'])
def view_index() :
  return render_template('index.html')


#http://localhost:5000/order/list
@app.route('/order/list', methods = ['GET']) #Enable GET and POST
def view_orders():	
  return json.loads( Order.objects.to_json() )
  
  # http://localhost:5000/package/list
@app.route('/package/list', methods = ['GET']) #Enable GET and POST
def view_packages():	
  return json.loads( Package.objects.to_json() )

# http://localhost:5000/order/new
@app.route('/order/new', methods = ['GET', 'POST'] )  
def place_order() :
 if(request.method == 'GET'):
  #print("sucks")
  return render_template('index.html')
   #print("porp")
 if (request.method=='POST'):

  #print("works")
  
  cust_name_val = request.form.get('customerName')
  cust_address_val = request.form.get('customerAddress')
  cust_region_val = request.form.get('customerRegion')
  cust_email_val = request.form.get('customerEmail')
  cust_phone_val = request.form.get('customerPhoneNo')
  package_val = request.form.get('packageNo')
  
  print( cust_name_val )
  print( cust_address_val )
  print( cust_region_val )
  print( cust_email_val, cust_phone_val )
  print( package_val )
  
  total = 0
  
  pkgesFound = Package.objects(pckid=package_val)
  pack = pkgesFound.first()
  
  print( pack, pack.pckid, pack.name, pack.price )
  total += int(pack.price)
  
  
  if cust_region_val == supported_regions[0] :
    total += supported_regions_delivery_cost[0]
  elif cust_region_val == supported_regions[1] :
    total += supported_regions_delivery_cost[1]
  elif cust_region_val == supported_regions[2] :
    total += supported_regions_delivery_cost[2]
  elif cust_region_val == supported_regions[3] :
    total += supported_regions_delivery_cost[3]
  elif cust_region_val == supported_regions[4] :
    total += supported_regions_delivery_cost[4]
  
  print( 'Total cost is', total)
  
  newOrder = Order( custName=cust_name_val, custAddress=cust_address_val, custRegion=cust_region_val, custEmail=cust_email_val,  pkgeNo=package_val, totPrice=total)
  
  newOrder.save()
  
  return 'Order successfully placed.  The total is $ ' + str( total ) + ' GYD.'
  
  
  

if __name__ == '__main__':
  app.run(debug=True)

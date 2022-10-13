import win32api
from flask import Flask,render_template,request,redirect
from flaskext.mysql import MySQL

app=Flask(__name__)
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='taller'
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/buscador')
def buscador():
    return render_template('buscador.html')


@app.route('/tabla')
def tabla():
    sql="SELECT * FROM `vehiculos`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    vehiculos=cursor.fetchall()
    print(vehiculos)
    conn.commit()
    return render_template('ingreso.html',vehiculos=vehiculos)
   

@app.route('/store',methods=['POST'])
def storage():
    placa=request.form['placa']
    marca=request.form['marca']
    modelo=request.form['modelo']
    color=request.form['color']
    nombre=request.form['nom']
    documento=request.form['doc']
    motivo=request.form['motivo']
    if placa=="" or marca=="" or modelo=="" or color=="" or nombre=="" or documento=="" or motivo=="":
        return redirect('/alert2')
    else:
        sql="INSERT INTO `vehiculos` (`placa`, `marca`, `modelo`, `color`, `propietario`, `docpropetario`, `consulta`, `estado`) VALUES (%s,%s ,%s ,%s ,%s ,%s ,%s ,'No reparado');"
    datos=(placa,marca,modelo,color,nombre,documento,motivo)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/alert1')


@app.route('/destroy/<int:id>')
def destroy(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM vehiculos WHERE id=%s",(id))
    conn.commit()
    return redirect('/alert3')


@app.route('/edit/<int:id>')
def editar(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM vehiculos WHERE id =%s",(id))
    vehiculos=cursor.fetchall()
    conn.commit()
    return render_template('update.html',vehiculos=vehiculos)


@app.route('/update',methods=['POST'])
def update():
    id=codigo=request.form['id']
    codigo=request.form['id']
    placa=request.form['placa']
    marca=request.form['marca']
    modelo=request.form['modelo']
    color=request.form['color']
    nombre=request.form['nom']
    documento=request.form['doc']
    motivo=request.form['motivo']
    estado=request.form['estado']
    if placa=="" or marca=="" or modelo=="" or color=="" or nombre=="" or documento=="" or motivo=="" or estado=="↓":
        return redirect('/alert5')
    else:
        sql="UPDATE vehiculos SET placa=%s, marca=%s, modelo=%s, color=%s, propietario=%s, docpropetario=%s, consulta=%s, estado=%s WHERE id=%s;"
    datos=(placa,marca,modelo,color,nombre,documento,motivo,estado,id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/alert4')


@app.route('/busqueda', methods=['POST'])
def busqueda():
    id=placa=request.form['placa']
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM vehiculos WHERE placa=%s",(id))
    vehiculos=cursor.fetchall()
    conn.commit()
    if placa=="":
        return redirect('/tabla')
    else:
        if len(vehiculos)==1:
            return render_template('ingreso.html',vehiculos=vehiculos)
        else:
            return redirect('/alert7')


@app.route('/buscar', methods=['POST'])
def buscar():
    id=placa=request.form['placa']
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM vehiculos WHERE placa=%s",(id))
    vehiculos=cursor.fetchall()
    conn.commit()
    if len(vehiculos)==1:
        return render_template('buscador.html',vehiculos=vehiculos)
    else:
        return redirect('/alert6')

    
@app.route('/alert1')
def alert1():
    win32api.MessageBox(0,'REGISTRO EXITOSO',' REGISTRO',0x00001000)
    return redirect('/buscador')    

@app.route('/alert2')
def alert2():
    win32api.MessageBox(0,'CAMPOS VACIOS',' REGISTRO',0x00001000)
    return redirect('/') 

@app.route('/alert3')
def alert3():
    win32api.MessageBox(0,'VEHICULO ELIMINADO',' ELIMINAR',0x00001000)
    return redirect('/tabla') 

@app.route('/alert4')
def alert4():
    win32api.MessageBox(0,'VEHICULO ACTUALIZADO',' ACTUALIZAR',0x00001000)
    return redirect('/tabla') 

@app.route('/alert5')
def alert5():
    win32api.MessageBox(0,'CAMPOS VACIOS',' ACTUALIZAR',0x00001000)
    return redirect('/tabla') 

@app.route('/alert6')
def alert6():
    win32api.MessageBox(0,'LA PLACA NO ESTA REGISTRADA',' BUSCAR',0x00001000)
    return redirect('/buscador') 


@app.route('/alert7')
def alert7():
    win32api.MessageBox(0,'LA PLACA NO ESTA REGISTRADA',' BUSCAR',0x00001000)
    return redirect('/tabla') 

if __name__=='__main__':
    app.run(debug=True)

    
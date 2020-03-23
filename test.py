







import json
import cgi, cgitb

import os, sys
import pandas as pd
import cgi, cgitb
import numpy as np
from os import getenv
import pyodbc
import os.path
import base_leer3 as bl3

import json
serial_origen_datos=0
correcto=1
#try:
import traceback
#
import datetime
import dateutil.relativedelta

#block warnings
import warnings
warnings.filterwarnings("ignore")


import requests
import random
import math
import base64
import hashlib
from requests_toolbelt.utils import dump 
import string
import secrets
#

import envio_correo as ec


import settings as st

import warnings
warnings.filterwarnings("ignore")



def fun_activar_pruebas():
    bl3.conf.gl_produccion=0


def fun_activar_produccion():
    bl3.conf.gl_produccion=1





def fun_trankey(data):
    if type(data) == str:
        
        sha1=hashlib.sha1(bytes(data,'utf-8')).hexdigest()
        trankey=base64.b64encode(bytes(sha1,'utf-8')).decode("utf-8")
    else:
        sha1=hashlib.sha1(data).digest()
        
        trankey=base64.b64encode(sha1).decode("utf-8")
    return trankey


def beauty_print(response): 
   
   prepared = dump.dump_all(response)
   print(prepared.decode('utf-8'))





        
        
def fun_consultar_plan(plan=5):
    
    try:
        consulta="""
        SELECT serial_place_pla, valor, periodicidad, maxPeriods,descripcion,currency,interval
        FROM dba_place_to_pay_planes
        WHERE serial_place_pla={plan}
        
        """.format(
            plan=plan
        )
#         print(consulta)
        df=bl3.conexion_base_sp(consulta)
        df=df[0]
        data={}
        if(not df.empty):
            data['valor']=df.loc[0,'valor']
            data['periodicidad']=df.loc[0,'periodicidad']
            data['maxPeriods']=df.loc[0,'maxPeriods']
            data['descripcion']=df.loc[0,'descripcion']
            data['currency']=df.loc[0,'currency']
            data['interval']=df.loc[0,'interval']
            data['serial_place_pla']=df.loc[0,'serial_place_pla']
        
        
        return data
    except Exception as e:
        st.gl_error.append(st.fun_error(e))
        
        
def fun_crear_venta_get_referencia():
    
    try:
        consulta="""
        DECLARE @serial_ventas int
        INSERT INTO dba_ventas (
            serial_prm,
            serial_llam_campana,
            serial_origen_datos,
            fecha
        )VALUES(

            36946,
            1,
            340,
            dateadd(HH,-5,GETUTCDATE())

        )
        set @serial_ventas=scope_identity()

        select @serial_ventas as serial_ventas

        select 1 as salida
        
        """.format(
        )
#         print(consulta)
        df=bl3.conexion_base_sp(consulta)
        serial_ventas=df[0].loc[0,'serial_ventas']
        serial_ventas=str(serial_ventas)
        return serial_ventas
    except Exception as e:
        st.gl_error.append(st.fun_error(e))



def fun_crear_session():

    
    try:
        data={}
        reference=fun_crear_venta_get_referencia()
        data=st.crear_credenciales()
        
        data['payment'] = {
                "reference": str(reference),
                "description": "Pago básico de prueba",
                "amount": {
                    "currency": "COP",
                    "total": "10000"
                    },
                "recurring": {
                "periodicity": "D",
                "interval": "1",
                "nextPayment": (datetime.datetime.utcnow() - dateutil.relativedelta.relativedelta(hours=5)+
        dateutil.relativedelta.relativedelta(days=1)).isoformat(),
                "maxPeriods": "12"
            }
            }

        data['expiration'] = (datetime.datetime.utcnow() - dateutil.relativedelta.relativedelta(hours=5)+
        dateutil.relativedelta.relativedelta(minutes=6)).isoformat()
        data["returnUrl"] = "http://52.184.182.178/pyt/placetopay/servicio_respuesta.py/5976030f5575d"
        data["ipAddress"]="127.0.0.1"
        data["userAgent"]="PlacetoPay eShop"
        

        response = requests.post(URL, data= json.dumps(data),headers=HEADER)

        response=json.loads(response.content)


        fun_insertar_respuesta(data['payment']['reference'],response,3)

        
        return response 
    except Exception as e:
        # print(e)
        st.gl_error.append(st.fun_error(e))
        
        
def fun_insertar_respuesta(reference,res,tipo=0,plan=0):
    
    
    try:
        consulta="""
        INSERT INTO dba_place_to_pay
        (
            reference,
            status,
            reason,
            message,
            fecha_creacion,
            requestId,
            serial_tipo_operacion_pasarela,
            serial_place_pla,
            activo,
            intentos_cobro,
            fecha_ultimo_cobro
            
            
            
        )
        VALUES (
            '{reference}',
            '{status}',
            '{reason}',
            '{message}',
             dateadd(HH,-5,GETUTCDATE()),
            '{requestId}',
            '{serial_tipo_operacion_pasarela}',
            {plan},
            1,
            0,
            '1900-01-01'
            
            


        )

        select 1 as salida
        
        """.format(
            reference= reference,
            status= res['status']['status'],
            reason= res['status']['reason'],
            message= res['status']['message'],
            fecha= res['status']['date'],
            requestId= res['requestId'],
            serial_tipo_operacion_pasarela=tipo,
            plan=plan
        )
#         print(consulta)
        df=bl3.conexion_base_sp(consulta)
    except Exception as e:
        st.gl_error.append(st.fun_error(e))
        
        
def fun_consultar_transaccion(requestId):
    try:
        requestId=str(requestId)
        data=st.crear_credenciales()        
     

        response = requests.post(URL+requestId, data= json.dumps(data),headers=HEADER)
#         beauty_print(response)


        return json.loads(response.content)
    except Exception as e:
        # print(e)
        st.gl_error.append(st.fun_error(e))
        
        
        
def fun_consultar_token_suscripcion(requestId):
    try:
        requestId=str(requestId)
        data=st.crear_credenciales()     
        data['reference']=requestId
     

        response = requests.post(URL, data= json.dumps(data),headers=HEADER)
#         beauty_print(response)


        return json.loads(response.content)
    except Exception as e:
        # print(e)
        st.gl_error.append(st.fun_error(e))
        
        
def fun_guardar_token_suscripcion():
    try:
        dict_respuesta=fun_consultar_transaccion(244460)
        token_suscripcion=dict_respuesta['subscription']['instrument'][0]['value']
        
    except Exception as e:
        st.gl_error.append(st.fun_error(e))
        
        
def fun_obtener_proximo_pago(periocidad):
    try:
        
        if(periocidad=='D'):
            ahora=datetime.datetime.utcnow() + dateutil.relativedelta.relativedelta(days=1)
            
        string = ahora.strftime("%Y-%m-%d")
        return string
    except Exception as e:
        # print(e)
        st.gl_error.append(st.fun_error(e))
        
        
def fun_crear_pago_recurrente(plan=5):
    try:
        data={}
        reference=fun_crear_venta_get_referencia()
        data=st.crear_credenciales()
        
        plan=fun_consultar_plan(plan)


        data['payment']={
            "reference": reference,
            "description": "Pago recurrente referencia: " +str(reference),
            "amount":{
                "currency": plan['currency'],
                "total": str(plan['valor'])
            },
            "recurring": {
                "periodicity": plan['periodicidad'],
                "interval": plan['interval'],
                "nextPayment": fun_obtener_proximo_pago('D'),
                "maxPeriods": plan['maxPeriods'],
                "notificationUrl":"http://52.184.182.178/pyt/placetopay/servicio_respuesta.py"
            }
        }

        data['expiration']=(datetime.datetime.utcnow() - dateutil.relativedelta.relativedelta(hours=5)+
        dateutil.relativedelta.relativedelta(minutes=6)).isoformat()

        data['returnUrl']=returnUrl
        data['ipAddress']=ipAddress
        data['userAgent']=userAgent




        response = requests.post(URL, data= json.dumps(data),headers=HEADER)

        response=json.loads(response.content)


        fun_insertar_respuesta(reference,response,2, plan['serial_place_pla'])
        return response
    except Exception as e:

        st.gl_error.append(st.fun_error(e))




        
def fun_calcular_proximo_cobro(fecha):
    try:
        aux = fecha
        aux = str(aux)
        aux= aux.replace('-','')
        fecha = datetime.datetime.strptime(aux[0:4]+"-"+aux[4:6]+"-"+aux[6:8], "%Y-%m-%d")
        
        
        now=datetime.datetime.now().strftime("%Y-%m-%d")
        if(fecha==now):
            respuesta=1
        else:
            respuesta=0


        #         fecha= fecha.replace("-", "")
        return fecha
    except Exception as e:
        st.gl_error.append(st.fun_error(e))
        print(e)
        
        
def fun_incrementar_desactivar_por_intentos_cobro(df_rechazados):
    try:
        
#         print(df_rechazados)
        # df_actualizar=df_rechazados[df_rechazados['intentos_cobro']<4]


        ######################################
        # las actualizaciones eran para intentar cobrar varias veces, al tenerlo vacio no se utiliza la funcionalidad
        ####################################
        df_actualizar=pd.DataFrame({'A' : []})

        ##############################3
        # Todo se inactiva
        ####################################
        df_inactivar=df_rechazados[df_rechazados['intentos_cobro']<4]
        
        if(not df_actualizar.empty):
            consulta="""
            DECLARE @json NVARCHAR(MAX)
            SET @json =  
                N'{json}' 

            update ptp
            set ptp.intentos_cobro=a.intentos_cobro
            FROM 
                OPENJSON ( @json ) 
            WITH (  
                        serial_place int '$.serial_place',
                        intentos_cobro int '$.intentos_cobro'
                ) a
                inner join dba_place_to_pay ptp on ptp.serial_place=a.serial_place          



            SELECT 1 as salida

            """.format(
                json=df_actualizar.to_json(orient='records')

            )
#             print(consulta)
            df=bl3.conexion_base_sp(consulta)
        
        if(not df_inactivar.empty):
            consulta="""
            DECLARE @json NVARCHAR(MAX)
            SET @json =  
                N'{json}' 

            update ptp
            set ptp.activo=0
            FROM 
                OPENJSON ( @json ) 
            WITH (  
                        serial_place int '$.serial_place',
                        intentos_cobro int '$.intentos_cobro'
                ) a
                inner join dba_place_to_pay ptp on ptp.serial_place=a.serial_place          
                inner join dba_ventas ven on ptp.serial_venta=ven.serial_venta

            where (select count(*) from dba_place_to_pay_notificaciones
		            where serial_venta=ptp.serial_venta and status='APPROVED'
		            )=0

            SELECT 1 as salida

            """.format(
                json=df_inactivar.to_json(orient='records')

            )
#             print(consulta)
            df=bl3.conexion_base_sp(consulta)
        
    except Exception as e:
        st.gl_error.append(st.fun_error(e))


def fun_crear_suscripcion():
    try:
        data={}
        reference=fun_crear_venta_get_referencia()
        data=st.crear_credenciales()
        
        
        data['subscription']={
            "reference": reference,
            "description": "Una suscripción de prueba"+str(reference)
        }
        
        data['expiration']=(datetime.datetime.utcnow() - dateutil.relativedelta.relativedelta(hours=5)+
        dateutil.relativedelta.relativedelta(minutes=6)).isoformat()
        
        data['returnUrl']=returnUrl
        data['ipAddress']=ipAddress
        data['userAgent']=userAgent
        
        
        
#         print(data)
        response = requests.post(URL, data= json.dumps(data),headers=HEADER)

        response=json.loads(response.content)


        fun_insertar_respuesta(data['subscription']['reference'],response,1,6)
        return response
    except Exception as e:
        print(e)
        st.gl_error.append(st.fun_error(e))



#LA SUSCRIPCION QUEDA PENDIENTE (BLOQUEADA) Y NO SE PUEDEN HACER NUEVOS COBROS
def fun_inserta_peticion_pendiente(data):
    
    try:
        import copy
        # print(data['payment']['reference'])
        data_aux= copy.deepcopy(data)  
        del data_aux['auth'] #BORRAR CREDENCIALES
        consulta="""
        UPDATE dba_place_to_pay 
        SET peticion_pendiente=1
        WHERE reference={reference}


        INSERT INTO dba_auditoria_pagos_detalle (json, fecha,serial_venta)
        VALUES
        ('{cadena_json}',dateadd(HH,-5,GETUTCDATE()),{serial_venta})


        SELECT 1 as salida

            """.format(
                reference= data['payment']['reference'],
                serial_venta=gl_serial_venta,
                cadena_json=json.dumps(data_aux)

            )
        df=bl3.conexion_base_sp(consulta)
        
    except Exception as e:
        st.gl_error.append(st.fun_error(e))            
#se recauda el pago a partir de una suscirpcion 
def fun_recaudar_pago(token,payer,referencia):
    global gl_serial_venta
    try:
        ####################################
        # CONSULTA SERIAL_VENTA
        #####################################
        consulta="""
        select cv.consecutivo,ptp.serial_venta from dba_place_to_pay ptp
        inner join dba_ventas ve on ve.serial_venta=ptp.serial_venta
        inner join dba_consecutivos_ventas cv on cv.serial_conventas=ve.serial_conventas
        where  cv.consecutivo={consecutivo}
         """.format(consecutivo= referencia)

        df=bl3.conexion_base_sp(consulta)
        gl_serial_venta = df[0].loc[0,'serial_venta']

        





        ############################
        if('email' in payer): 
            email=payer['email']
        else:
            email=''            
        
        if('surname' in payer):
            surname=payer['surname']
        else:
            surname=''
        
        if('document' in payer):
            document=payer['document']
        else:
            document=''
        if('name' in payer):
            name=payer['name']
        else:
            name=''
        if('documentType' in payer):
            documentType=payer['documentType']
        else:
            documentType=''

        
        data=st.crear_credenciales()
        
        ###################
        # IMPUESTO 5%
        ##################################33}
        # print(payer['valor'])
        tax=0.05*int(payer['valor'])/1.05

        
        data['instrument']={
        "token": {
            "token": token
            }
        }
        data['payer']={
        "document": document,
        "documentType": documentType,
        "name": name,
        "surname": surname,
        "email": email
        }
        data['payment']={
        "reference": str(referencia),
        "description": "Pago con suscripción " +str(referencia) , 
        "amount": {
            "currency": payer['currency'],
            "total": str(payer['valor']).split(".")[0] ,   #QUITAR DECIMALES JSON NO SERIALISABLE
            "taxes": [
                        {
                        "kind": "valueAddedTax",
                        "amount": tax,
                        "base": 5
                        }
                    ]         
            }
            
        }
        
        #######################################3
        # INSERTA EN DB TRANSACCION PENDIENTE
        #############################################

        fun_inserta_peticion_pendiente(data)

        response = requests.post(URL_COLLECT, data= json.dumps(data),headers=HEADER)
#         beauty_print(response)
#         print(data)

        ##############################################
        # SI NO CONTESTA ES ERROR 524 Y NO SE HACE NADA PUES LA PETICION YA FUE ENVIADA, QUEDA BLOQUEADA LA SUSCRIPCION
        #############################################
        try:
            response=json.loads(response.content)
            #         print(response)
            ####################################################
            #### VARIABLES
            ####################################################
            variables={}
            variables['monto']=response['request']['payment']['amount']['total']
            variables['currency']=response['request']['payment']['amount']['currency']
            variables['requestId']=response['requestId']   
            variables['reference']=response['request']['payment']['reference']      
            
            ##
            variables['status']=response['status']['status']
            variables['reason']=response['status']['reason']
            variables['message']=response['status']['message']
            
            
            
            ####################################################
            #### ACTUALIZAR
            ##################################################
            fun_insertar_peticion_pago(variables)
        
        except Exception as e:
            # print(e)
            pass

        # print(variables)
        # print(response)
        return response
    except Exception as e:
        st.gl_error.append(st.fun_error(e))
        
def fun_insertar_peticion_pago(variables):
    
    try:
        ##########################################
        # CONSULTA serial_venta CON CONSECUTIVO
        ############################################
        consulta="""
        select consecutivo ,ve.serial_venta
		from dba_ventas ve
		inner join dba_consecutivos_ventas cv on cv.serial_conventas=ve.serial_conventas
		where cv.consecutivo={consecutivo}

        
        """.format(
            consecutivo= variables['reference'],

        )
        df=bl3.conexion_base_sp(consulta)
        serial_venta=df[0].loc[0,'serial_venta']



        ###################################################


        consulta="""
        SELECT requestId
        FROM dba_place_to_pay_notificaciones
        WHERE requestId={requestId}
        select 1 as salida
        
        """.format(requestId=variables['requestId'])
        df=bl3.conexion_base_sp(consulta)

        df=df[0]
        if(not df.empty):
            accion='UPDATE'
        else:
            accion='INSERT'
            
        if(accion=='INSERT'):
#         print(variables)
            consulta="""
            INSERT INTO dba_place_to_pay_notificaciones
            (
                reference,
                status,
                reason,
                message,
                fecha_creacion,
                requestId,
                viene_de_place_to_play,
                valor,
                currency
            )
            VALUES (
                '{reference}',
                '{status}',
                '{reason}',
                '{message}',
                dateadd(HH,-5,GETUTCDATE()),
                '{requestId}',
                {viene_de_place_to_play},
                {valor},
                '{currency}'
            )


            update pp set pp.cartera=0 from 
            dba_ventas ven inner join dba_paciente_plan pp
            on ven.serial_ppac=pp.serial_ppac
            where ven.serial_venta={reference} and '{status}'='APPROVED'

            update pp set pp.cartera=0 from 
            dba_ventas ven inner join dba_paciente_plan pp
            on ven.serial_ppac=pp.serial_ppac_prin
            where ven.serial_venta={reference} and '{status}'='APPROVED'

            UPDATE dba_place_to_pay
            SET peticion_pendiente=0
            WHERE reference='{reference}'



            SELECT 1 as salida

            """.format(

                reference= serial_venta,
                status= variables['status'],
                reason= variables['reason'],
                message= variables['message'],
                requestId= variables['requestId'],
                viene_de_place_to_play=2,            
                valor=variables['monto'],            
                currency=variables['currency']


            )
    #         print(consulta)
        else:
            consulta="""
            UPDATE dba_place_to_pay_notificaciones
            SET valor= {valor}, currency='{currency}'
            WHERE requestId = '{requestId}'

            select 1 as salida

            """.format(
                reference= serial_venta,
                
                
                requestId= variables['requestId'],
                       
                valor=variables['monto'],            
                currency=variables['currency']
            )
#             print(consulta)
        # print(consulta)    
        df=bl3.conexion_base_sp(consulta)
    except Exception as e:
        # print(e)
        st.gl_error.append(st.fun_error(e))



########### TRNSACCIONS ACTIVAS Y SIN BLOQUEOS
def fun_consultar_suscripciones_activas(reference_id):
    try:
        filtrar=''
        # filtrar= "and ptp.reference_id='378B9879-ED55-4B86-9F08-1294F32DGSDGS'"
        if(reference_id != ''):
            ###########################################3
            # COBRA LA PRIMERA VEZ
            ###################################################
            filtrar= " and ptp.reference_id='{reference_id}'".format(reference_id=reference_id)
            consulta="""
            SELECT 0 AS dias_debe,ptp.serial_place,ven.serial_venta, 0 as dias_ultimo_pago_debe ,
            ISNULL(ptp.fecha_ultimo_cobro,'1900-01-01') as fecha_ultimo_cobro,
            ptp.fecha_prox_cobro,ptp.reference,requestId, ptpp.periodicidad,
            ptp.fecha_creacion,
            ISNULL(ptp.intentos_cobro,'0') as intentos_cobro,
            ptpp.currency,ptp.peticion_pendiente,
            dbo.Fn_Consulta_Valor_Prima_New(ven.serial_ppac,1)*1.05 as valor,
            (select count(*) from dba_place_to_pay_notificaciones
            where serial_venta=ptp.serial_venta and status='APPROVED') as cantidad_efectivos, 1 as altura, 0 as altura_paga, 0 as dias_despues,
            0 as intentos_altura
            FROM dba_place_to_pay ptp
            INNER JOIN dba_place_to_pay_planes ptpp ON ptpp.serial_place_pla=ptp.serial_place_pla
            inner join dba_ventas ven on ptp.serial_venta=ven.serial_venta
            inner join dba_paciente_plan pp on ven.serial_ppac=pp.serial_ppac
            WHERE ptp.serial_tipo_operacion_pasarela=1 and ptp.activo=1 
            and ISNULL(ptp.peticion_pendiente,0)=0 and pp.activo=1 
            


            
            {filtrar}
            """.format(filtrar=filtrar)
        ###################
        # COBROS RECURSIVOS
        #
        else:
            consulta="""
            declare @fecha_actual datetime
            set @fecha_actual=dateadd(HH,-5, getutcdate())
            

            SELECT 
                ISNULL(DATEDIFF(day,(SELECT top 1 fecha_creacion from dba_place_to_pay_notificaciones 
		        where serial_venta=ven.serial_venta AND status='APPROVED' order by serial_place_not DESC ) ,@fecha_actual ),0) as dias_debe,
                ptp.reference_id,
                (select count(*) from dba_intentos_cobro where altura=
                (1+dbo.fn_mes_diferencia(ptp.fecha_creacion,@fecha_actual)
                ) and serial_venta=ven.serial_venta
                ) as intentos_altura,
                1+dbo.fn_mes_diferencia(ptp.fecha_creacion,@fecha_actual) as altura,
                (select ISNULL(max(altura),1) from dba_intentos_cobro where serial_venta=ven.serial_venta
                and estado=1
                ) as altura_paga,
                datediff(DD,
                dateadd(MM,1-(select ISNULL(max(altura),1) from dba_intentos_cobro where serial_venta=ven.serial_venta
                and estado=1
                ),ptp.fecha_creacion),@fecha_actual)
                
                as dias_ultimo_pago_debe,
                ptpp.serial_place_pla,DATEPART(dw,@fecha_actual) as dia_semana,
                datediff(DD,dateadd(MM,dbo.fn_mes_diferencia(ptp.fecha_creacion,@fecha_actual),ptp.fecha_creacion),@fecha_actual) as dias_despues,
                
                
                ptp.serial_place,ven.serial_venta,
                ISNULL(ptp.fecha_ultimo_cobro,'1900-01-01') as fecha_ultimo_cobro,
                ptp.fecha_prox_cobro,ptp.reference,requestId, ptpp.periodicidad,
                ptp.fecha_creacion,
                ISNULL(ptp.intentos_cobro,'0') as intentos_cobro,
                ptpp.currency,ptp.peticion_pendiente,
                dbo.Fn_Consulta_Valor_Prima_New(ven.serial_ppac,1)*1.05 as valor,
                (select count(*) from dba_place_to_pay_notificaciones
                where serial_venta=ptp.serial_venta and status='APPROVED') as cantidad_efectivos
                FROM dba_place_to_pay ptp
                INNER JOIN dba_place_to_pay_planes ptpp ON ptpp.serial_place_pla=ptp.serial_place_pla
                inner join dba_ventas ven on ptp.serial_venta=ven.serial_venta
                inner join dba_paciente_plan pp on ven.serial_ppac=pp.serial_ppac
                WHERE ptp.serial_tipo_operacion_pasarela=1 and ptp.activo=1 
                and ISNULL(ptp.peticion_pendiente,0)=0 and pp.activo=1 
                and 
                
                ((select count(*) from dba_place_to_pay_notificaciones
                where serial_venta=ptp.serial_venta and status='APPROVED'
                )-1)
                <
                convert(int,dbo.fn_mes_diferencia(ptp.fecha_creacion,@fecha_actual)/ptpp.meses)


                and (select count(*) from dba_place_to_pay_notificaciones
                where serial_venta=ptp.serial_venta and status='APPROVED'
                )>0 

                UNION
                SELECT 
                ISNULL(DATEDIFF(day,(SELECT top 1 fecha_creacion from dba_place_to_pay_notificaciones 
		        where serial_venta=ven.serial_venta AND status='APPROVED' order by serial_place_not DESC ) ,@fecha_actual ),0) as dias_debe,
                ptp.reference_id,
                (select count(*) from dba_intentos_cobro where altura=
                (1+dbo.fn_mes_diferencia(ptp.fecha_creacion,@fecha_actual)
                ) and serial_venta=ven.serial_venta
                ) as intentos_altura,
                1+dbo.fn_mes_diferencia(ptp.fecha_creacion,@fecha_actual) as altura,
                (select ISNULL(max(altura),0) from dba_intentos_cobro where serial_venta=ven.serial_venta
                and estado=1
                ) as altura_paga,
                datediff(DD,
                dateadd(MM,1-(select ISNULL(max(altura),1) from dba_intentos_cobro where serial_venta=ven.serial_venta
                and estado=1
                ),ptp.fecha_creacion),@fecha_actual)
                
                as dias_ultimo_pago_debe,
                ptpp.serial_place_pla,DATEPART(dw,@fecha_actual) as dia_semana,
                datediff(DD,dateadd(MM,dbo.fn_mes_diferencia(ptp.fecha_creacion,@fecha_actual),ptp.fecha_creacion),@fecha_actual) as dias_despues,
                
                
                ptp.serial_place,ven.serial_venta,
                ISNULL(ptp.fecha_ultimo_cobro,'1900-01-01') as fecha_ultimo_cobro,
                ptp.fecha_prox_cobro,ptp.reference,requestId, ptpp.periodicidad,
                ptp.fecha_creacion,
                ISNULL(ptp.intentos_cobro,'0') as intentos_cobro,
                ptpp.currency,ptp.peticion_pendiente,
                dbo.Fn_Consulta_Valor_Prima_New(ven.serial_ppac,1)*1.05 as valor,
                (select count(*) from dba_place_to_pay_notificaciones
                where serial_venta=ptp.serial_venta and status='APPROVED') as cantidad_efectivos
                FROM dba_place_to_pay ptp
                INNER JOIN dba_place_to_pay_planes ptpp ON ptpp.serial_place_pla=ptp.serial_place_pla
                inner join dba_ventas ven on ptp.serial_venta=ven.serial_venta
                inner join dba_paciente_plan pp on ven.serial_ppac=pp.serial_ppac
                WHERE ptp.serial_tipo_operacion_pasarela=1 and ptp.activo=1 
                and ptp.fecha_ultimo_cobro='1900-01-01 00:00:00.000'
				and (select ISNULL(max(altura),0) from dba_intentos_cobro where serial_venta=ven.serial_venta
                and estado=1
                ) =0 --que no hayan pagado ninguna vez
          



                SELECT 1 as salida
            
            """.format(filtrar=filtrar)
        # print(consulta)

        
        df=bl3.conexion_base_sp(consulta)
        df=df[0]
        if(not df.empty):
            df['fecha_ultimo_cobro']=df['fecha_ultimo_cobro'].fillna(0)
            df['fecha_prox_cobro']=df['fecha_prox_cobro'].fillna(0)
        else:
            pass
            # st.gl_error.append("Sin suscripciones")
            # st.gl_error.append(consulta)
        return df
    except Exception as e:
        st.gl_error.append(st.fun_error(e))
    
 
        
def fun_desactivar_suscripcion_por_expiracion(reference):
    try:
        consulta="""
        UPDATE dba_place_to_pay
        SET activo=0
        WHERE reference='{reference}'

        select 1 as salida
        
        """.format(reference=reference
            
        )
#         print(consulta)
        df=bl3.conexion_base_sp(consulta)
        
    except Exception as e:
        st.gl_error.append(st.fun_error(e))


def fun_actualizar_cobros_aprobados(df_aprobados):
    try:
        
        df_aprobados=df_aprobados[['reference']]
        consulta="""
        
        
        
        
        DECLARE @json NVARCHAR(MAX)
        SET @json =  
            N'{cadena_json}' 

        update ptp set ptp.fecha_ultimo_cobro=dateadd(HH,-5,GETUTCDATE())
        FROM 
            OPENJSON ( @json ) 
        WITH (  
                    reference   varchar(200) '$.reference' 
            ) a
            inner join dba_place_to_pay ptp on a.reference= ptp.reference


        
        select 1 as salida
        
        """.format(cadena_json=df_aprobados.to_json(orient='records')
            
        )
#         print(consulta)
        df=bl3.conexion_base_sp(consulta)
        
    except Exception as e:
        st.gl_error.append(st.fun_error(e))




# PENDIENTE 1 NO PENDIENTE 0
def fun_revisar_pendientes(reference):
    try:
        ##############################################
        # CONSULTAR SI PENDIENTE
        #####################################
        consulta="""
        SELECT status,requestId,fecha_creacion FROM dba_place_to_pay_notificaciones
        WHERE reference='{reference}' and status='PENDING'
        
        
        SELECT intentos_cobro  FROM dba_place_to_pay
        WHERE reference='{reference}' 

        
        
        select 1 as salida
        
        """.format(reference=reference
            
        )
        
        df_querys=bl3.conexion_base_sp(consulta)
        
        df=df_querys[0]
#         print(df)
        if df.empty:            
            respuesta=0
        else:
            respuesta=1
            ######################################
            # GESTIONAR PENDIENTE
            ########################################
            # print(int(df_querys[1].loc[0,'intentos_cobro']))
            fecha_creacion=df_querys[0].loc[0,'fecha_creacion']
            ahora = datetime.datetime.now() - dateutil.relativedelta.relativedelta(days=3)
            fecha_limite= fecha_creacion >ahora
            if((int(df_querys[1].loc[0,'intentos_cobro'])   <60) and (fecha_limite)   ):


                estado_transaccion=fun_consultar_transaccion(df.loc[0,'requestId'])
                
                ################################################
                # AUMENTAR intentos_cobro
                ################################
                if(estado_transaccion['status']['status']=='PENDING'):
                    consulta="""

                         UPDATE dba_place_to_pay
                         SET intentos_cobro=intentos_cobro+1
                         WHERE reference='{reference}'                 





                        select 1 as salida

                        """.format(reference=reference

                        )

                    df=bl3.conexion_base_sp(consulta)
                    
                #######################################################
                # ACTUALIZAR ESTADO PETICION
                #############################################################
                else:
                    consulta="""

                         UPDATE dba_place_to_pay_notificaciones
                         SET status='{status}', 
                         WHERE requestId='{requestId}'                

                        select 1 as salida

                        """.format(status=estado_transaccion['status']['status'],
                                   requestId=df.loc[0,'requestId']
                                   

                        )

                    df=bl3.conexion_base_sp(consulta)
            ###############################################################
            # INACTIVAR SUSCRIPCION
            #############################################
            else:                
                consulta="""
                UPDATE dba_place_to_pay
                SET activo=0
                WHERE reference='{reference}' 

                UPDATE dba_place_to_pay_notificaciones
                SET status='REJECTED', message='Transacción cancelada por EDENTAL (Sin respuesta para transacción pendiente)'
                WHERE requestId='{requestId}'   

                select 1 as salida

                """.format(reference=reference,
                    requestId=df.loc[0,'requestId']
                )
                df=bl3.conexion_base_sp(consulta)         
                
                
            
            
        
        return respuesta
    except Exception as e:
        st.gl_error.append(st.fun_error(e))


def fun_poner_cartera(serial_venta):
    try:
        consulta=""" 
        update pp set pp.cartera=0 from 
        dba_ventas ven inner join dba_paciente_plan pp
        on ven.serial_ppac=pp.serial_ppac
        where ven.serial_venta={serial_venta} 
        
        select 1 as salida
        """.format(serial_venta=serial_venta)
        df=bl3.conexion_base_sp(consulta)
    except Exception as e:
        st.gl_error.append(st.fun_error(e))


def fun_excluir(serial_venta):
    try:
        consulta=""" 
        update pp set pp.activo=0, pp.Fecha_Exclusion=dateadd(HH,-5,GETUTCDATE()),  serial_texc= 6     
        from dba_ventas ven 
        inner join dba_paciente_plan pp on ven.serial_ppac=pp.serial_ppac
        where ven.serial_venta={serial_venta} 

        update dba_place_to_pay set activo =0 
        where serial_venta = {serial_venta} 
        
        select 1 as salida
        """.format(serial_venta=serial_venta)
        df=bl3.conexion_base_sp(consulta)
    except Exception as e:
        st.gl_error.append(st.fun_error(e))

def fun_revisar_si_cobrar(intentos_altura,altura,altura_paga, dias_despues,valor,serial_venta):
    try:
        # DIAS DESPUES ES DIAS_DEBE


        ########################################
        # COBRAR SI/NO
        #######################################
        cobrar_final=0
        valor_final=0
        if(intentos_altura==0):
            cobrar_final=1
        if(dias_despues>36):
            #SOLO COBRA AL DIA 35 Y 40 
            if(dias_despues==37 or dias_despues==40):
                cobrar_final=1
            #PONER EN CARTERA
            fun_poner_cartera(serial_venta)
        # EXCLUIR
        elif(dias_despues>89):
            fun_excluir(serial_venta)
        
        
        #############################################3
        # VALOR A COBRAR
        ############################################
        
        valor_final=(altura-altura_paga)*valor
    
        if valor_final== 0:
            cobrar_final=0

        #########################
        #FILTRO SEGURIDAD
        ############################3
        if(altura-altura_paga>3):
            cobrar_final=0
            st.gl_error.append("Cantidad de cobros excesivo: "+str(altura-altura_paga))



        cantidad_cuotas=altura-altura_paga

        

        return cobrar_final, valor_final,cantidad_cuotas
    except Exception as e:
        st.gl_error.append(st.fun_error(e))
        return 0,0

def fun_insertar_auditoria(data):
    try:
        consulta=""" 
        INSERT INTO dba_auditoria_pagos (json,fecha)
        VALUES
        ('{cadena_json}',dateadd(HH,-5,GETUTCDATE()))

        select 1 as salida
        """.format(cadena_json=data.to_json(orient="records"))
        df=bl3.conexion_base_sp(consulta)
    except Exception as e:
        st.gl_error.append(st.fun_error(e))

def fun_cobrar_suscripciones(df_suscripciones):
    try:

        #ALTURA CUOTA QUE ESTA PAGANDO (CONSECUTIVO)
        #ALTURA_PAGA CUOTAS QUE HA PAGADO

        #######################################3
        # COBROS
        ###########################################

        # COBRAR POR ALTURA

        # INTENTOS ALTURA = 0 COBRAR
        # ¿CUANTO COBRAR? ALTURA-ALTURA_PAGO * VALOR (ALTURA INT, PERIODOS QUE DEBERIA TENER PAGADO,ALTURA_PAGO, PERIODOS PAGOS)
        # INSERTAR LOS INTENTOS COBRO, dba_intentos_cobro 

        # COBRAR POR DIAS DESPUES
        
        # COBRAR POR dias_despuesta = 5 (cartera=1) o 10 (cartera=1)
        # dias_despuesta = 90 Excluye




        obj={}
        n=0        
        #(intentos_altura,altura,altura_paga, dias_despues,valor)

        df_suscripciones[['cobrar', 'valor','cantidad_cuotas']] = df_suscripciones.apply(
            lambda x: pd.Series(fun_revisar_si_cobrar( x['intentos_altura'],x['altura']
            ,x['altura_paga'], x['dias_debe'],x['valor'],x['serial_venta']
            )), axis=1)

        #cobrar a todo lo que llega
        # df_suscripciones['cobrar']=1
        df_suscripciones['status_actual']='SIN ACCIÓN'
        while n<len(df_suscripciones):
            if(df_suscripciones.loc[n,'cobrar']==1):
                ##########################################
                #CONSULTA SUSCRIPCION, SI ESTA REJECTED (TIEMPO ESPERA SE SUPERO) LA RECHAZA
                ########################################################
                dict_respuesta=fun_consultar_transaccion(df_suscripciones.loc[n,'requestId'])
    
                #if(dict_respuesta['status']['status']=='REJECTED'):
                    #fun_desactivar_suscripcion_por_expiracion(df_suscripciones.loc[n,'reference'])


                ##################################################
                # SUSCRIPCION ACTIVA EN EL MOMENTO
                #########################################################
                if(dict_respuesta['status']['status']=='PENDING' or dict_respuesta['status']['status']=='REJECTED'):
                    df_suscripciones.loc[n,'status_actual']='NO SUSCRIBE'
                    fun_insertar_intentos_cobro(
                            json_dict='[{"motivo":"La suscripcion no se encuentra activa"}]',
                            consecutivo=dict_respuesta['request']['subscription']['reference'],
                            altura=df_suscripciones.loc[n,'altura'],
                            estado= df_suscripciones.loc[n,'status_actual'],
                            requestId = dict_respuesta['requestId'], #es el mismo requestid de la suscripcion
                            cantidad_cuotas=df_suscripciones.loc[n,'cantidad_cuotas']

                                )
                ########################################################
                #SI SUSCRIPCION ESTÁ ACTIVA
                #########################################################
                else:

                    ###########################################################
                    # REVISAR PENDIENTES
                    # #################################################################
                    # PENDIENTE =1 NO PENDIENTE=0, inactiva el estado dependiente luego de 3 (consultas)
                    suscripcion_pendiente=fun_revisar_pendientes(df_suscripciones.loc[n,'reference'])

                    if(suscripcion_pendiente==1):
                        df_suscripciones.loc[n,'status_actual']='PENDING'

                    else:
                        #TRATA DE COBRAR
                        try:
                            referencia=dict_respuesta['request']['subscription']['reference']
                            token_sus=dict_respuesta['subscription']['instrument'][0]['value']
                            payer=dict_respuesta['request']['payer']

                            #############################################3
                            # VALOR Y CURRENCI
                            ################################################
                            payer['valor']=df_suscripciones.loc[n,'valor']
                            payer['currency']=df_suscripciones.loc[n,'currency']


                            ###################################
                            # GENERA INTENTO DE COBRO
                            ###########################
                            try:
                                
                                json_res=fun_recaudar_pago(token_sus,payer,referencia)
                                
                                #PARA PRUEBAS:
                                # json_res ={}
                                # json_res['status']={}                                
                                # json_res['status']['status']='STATUS'                                
                                # json_res['requestId']=1

                                # print(json_res)
                                df_suscripciones.loc[n,'status_actual']=json_res['status']['status']
                                
                                #FALLOS POR ALGUN MOTIVO
                                if(json_res['status']['status']=='FAILED'):
                                    status='REJECTED'
                                    requestId=0
                                    message=json_res['status']['message']
                                    fun_insertar_rechazado(referencia,status,json_res,message)
                                else:
                                    requestId = json_res['requestId']

                                #INSERTAR INTENTOS DE COBRO
                                fun_insertar_intentos_cobro(
                                json_dict=json_res,
                                consecutivo=referencia,
                                altura=df_suscripciones.loc[n,'altura'],
                                estado= df_suscripciones.loc[n,'status_actual'],
                                requestId = requestId,
                                cantidad_cuotas=df_suscripciones.loc[n,'cantidad_cuotas']

                                 )
                            except Exception as e:
                                st.gl_error.append(json_res)
                                st.gl_error.append(st.fun_error(e))
                                df_suscripciones.loc[n,'status_actual']='ERROR'
                            ###################
                            # ESTADO TRANSACCION
                            ################
                            
                        except Exception as e:
                            #SI EL CLIENTE CANCELO EL PROCESO DE PAGO, DEJAR LA TRNSACCION COMO RECHAZADA
                            if "status" in dict_respuesta.keys() and "reason" in dict_respuesta["status"].keys() and dict_respuesta["status"]["reason"]=="?C" :
                                consulta="""
                                UPDATE dba_place_to_pay SET message='La petición ha sido cancelada por el usuario',status='REJECTED',
                                reason='?C' where serial_venta=(
                                SELECT TOP 1 serial_venta FROM dba_ventas ve 
                                inner join dba_consecutivos_ventas cv on cv.serial_conventas=ve.serial_conventas
                                WHERE cv.consecutivo={consecutivo})

                                select 1 as salida
                                """.format(
                                    consecutivo=dict_respuesta["request"]["subscription"]["reference"]
                                )
                                # st.gl_error.append(consulta)  
                                df=bl3.conexion_base_sp(consulta)
                            #SI NO LA DEJO COMO RECHAZADA, ERROR
                            else: 
                                                                  
                                st.gl_error.append("Intento de cobro: "+str(n))                            
                                st.gl_error.append(st.fun_error(e))
                                # st.gl_error.append(dict_respuesta)
                                st.gl_error.append({"requestId":df_suscripciones.loc[n,'requestId']})

                    
                
                # print(n)
            n=n+1
            
            
            
        
        
        df_rechazados=df_suscripciones[df_suscripciones['status_actual']=='REJECTED']
        df_aprobados=df_suscripciones[df_suscripciones['status_actual']=='APPROVED']
        # df_pendientes=df_suscripciones[df_suscripciones['status_actual']=='PENDING']

#         if(not df_rechazados.empty):
#             df_rechazados['intentos_cobro']=df_rechazados['intentos_cobro'].apply(lambda x: int(x)+1)
# #             df_suscripciones[df_suscripciones['status_actual']=='REJECTED']=df_suscripciones['intentos_cobro'].apply(lambda x: int(x)+1)
#             fun_incrementar_desactivar_por_intentos_cobro(df_rechazados)
    
        if(not df_aprobados.empty):
            fun_actualizar_cobros_aprobados(df_aprobados)
            
                    

                    
                    
                
            
        fun_insertar_auditoria(df_suscripciones)     
        return df_suscripciones
    except Exception as e:
        st.gl_error.append(st.fun_error(e))


def fun_insertar_rechazado(consecutivo,status,cadena_json,message):
    try:

        consulta="""
        select consecutivo ,ve.serial_venta
		from dba_ventas ve
		inner join dba_consecutivos_ventas cv on cv.serial_conventas=ve.serial_conventas
		where cv.consecutivo={consecutivo}

        
        """.format(
            consecutivo= consecutivo,

        )
        df= bl3.conexion_base_sp(consulta)
        serial_venta = df[0].loc[0,'serial_venta']
        consulta="""
            INSERT INTO dba_place_to_pay_notificaciones
            (
                reference,
                status,
                reason,
                message,
                fecha_creacion,
                requestId,
                signature,
                json,
                viene_de_place_to_play

            )
            VALUES (
                '{reference}',
                '{status}',
                'RE',
                '{message}',
                dateadd(HH,-5,GETUTCDATE()),
                '0',
                '0',
                '{cadena_json}',
                1



            
            )
            
            select 1 as salida
            """.format(
                status='REJECTED',
                cadena_json=json.dumps(cadena_json),
                reference=serial_venta,
                message=message
            )
        # print(consulta)
        df=bl3.conexion_base_sp(consulta)
    except Exception as e:
        st.gl_error.append(st.fun_error(e))

def fun_insertar_intentos_cobro(json_dict,consecutivo,altura,estado,requestId,cantidad_cuotas):


    global gl_error
    try:

        #CONSULTA SERIAL VENTA
        consulta="""
        select consecutivo ,ve.serial_venta
		from dba_ventas ve
		inner join dba_consecutivos_ventas cv on cv.serial_conventas=ve.serial_conventas
		where cv.consecutivo={consecutivo}

        
        """.format(
            consecutivo= consecutivo,

        )
        df= bl3.conexion_base_sp(consulta)
        serial_venta = df[0].loc[0,'serial_venta']

        #####################################
        # INSERTA INTENTOS DE COBRO
        ###################################333
        estado_h = 1  if estado == 'APPROVED' else 0
        consulta= """
        INSERT INTO dba_intentos_cobro (serial_venta,estado,json,fecha,altura,cantidad_cuotas,requestId)
        VALUES
        ({serial_venta}, {estado},'{json}',dateadd(HH,-5,GETUTCDATE()),{altura},{cantidad_cuotas},{requestId})

        select 1 as salida
        """.format(
        serial_venta=serial_venta,
        estado=estado_h,
        json= json.dumps(json_dict) ,
        altura=altura,
        cantidad_cuotas=cantidad_cuotas,
        requestId=requestId)
        # print(consulta)
        df=bl3.conexion_base_sp(consulta)
    except Exception as e:
        st.gl_error.append(st.fun_error(e))



#############################################################################
#MAIN
###############################################################################

def main(reference_id=''):
    
    
    df=pd.DataFrame({'A' : []})
    try:
        df_suscripciones=fun_consultar_suscripciones_activas(reference_id)
        if(not df_suscripciones.empty):
            df=fun_cobrar_suscripciones(df_suscripciones)
        else:

            pass
            # st.gl_error.append('Sin suscripciones')
    except Exception as e:
        st.gl_error.append(st.fun_error(e))




    if(len(st.gl_error)==0):
        
        proceso='Cobro realizado'
        if(not df.empty):
            contenido=df.to_html()
        else:
            contenido='Sin suscripciones activas para este pedido '+reference_id
    else:
        proceso='PLACETOPLAY [Cobros con error]'
        if(not df.empty):
            contenido=df.to_html()+"<br> ERRORES:<br> " +str(st.gl_error)
        else:
            contenido=str(st.gl_error)






    try:
        ec.envio_mail('jmarin@e-dentalsys.com',
                    '',
                    proceso,
                    contenido,
                    '',
                    '',
                    'smtp.gmail.com','465',
                    'info@e-dentalsys.com','Temporal1*')

            
    except Exception as e:
        st.gl_error.append(st.fun_error(e))

    
    return df
    # print('Errores:'+ str(st.gl_error))


#####################################################################################
###VARIABLES
#####################################################################################


def fun_init_variables():
    global URL  
    global URL_PAGO
    global returnUrl
    global ipAddress
    global userAgent
    global login
    global secretkey
    global HEADER
    global data
    
    global URL_COLLECT

    URL= st.URL
    URL_PAGO=st.URL_PAGO
    URL_COLLECT=st.URL_COLLECT
    returnUrl=st.returnUrl
    ipAddress=st.ipAddress
    userAgent=st.userAgent 


    login=st.LOGIN
    secretkey=st.SECRETKEY

    HEADER=st.HEADER

    data={}
    # st.gl_error=[]


#POST /api/session

if __name__ == "__main__":
    print("HTTP/1.1 200 OK")
    print("Access-Control-Allow-Origin: *")
    print("Content-Type: text/json\n")
    fun_init_variables()
    main()


fun_init_variables()
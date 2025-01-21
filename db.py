import sys,cx_Oracle
from paramiko import SSHClient

print("DB import automation",sys.argv[0])
print("Argument List:", str(sys.argv))
arglist=sys.argv[1:]
try:
    client = SSHClient()
    client.connect(str(arglist[0]),username=str(arglist[1]), password=str(arglist[2]))
except:
    print("connected to host ")

try:
    conn_str = u'import_export/impexpus3r/orclpdb'
    conn = cx_Oracle.connect(conn_str)
    
    c = conn.cursor()
except:
    print("connected to sql")    
try:
    c.execute(u"set echo on serveroutput on; begin manh_import( p_project_code => 'KUEH', p_email_id => 'sjayachandran@manh.com', p_dmp_dir => 'dmp', p_dmp_file => 'expdp_cso12r1b__KUEH2017WMDEV-KUEH2017WMDEV_LMDA__20220217_023508.dmp',p_source_schemas => 'KUEH2017WMDEV,KUEH2017WMDEV_LMDA',p_target_schemas => 'KUEH2018WMSANTDEV,KUEH2018WMSANTDEV_LMDA'); end;/")
except:
    print("import successful")

    conn.close()

    
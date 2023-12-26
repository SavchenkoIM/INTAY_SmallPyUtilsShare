
import pandas as pd
from projectFile import projectFile
from makeIniOutputFile import makeIniOutputFile

f = makeIniOutputFile('D:\\anpar.txt', True)

### Building vector AnPar
#projectFile = pd.Series({'AnPar': anpar.ANPAR, 'INFO_AGREGAT': 'ПТ1'})
### Building vector AnPar

#f = makeIniOutputFile(destFile, True)

f += ('''
<?xml version="1.0" encoding="utf-8"?>
<project xmlns="http://www.plcopen.org/xml/tc6_0200">
    <fileHeader companyName="Prosoft - Systems" productName="Epsilon LD" productVersion="Epsilon LD V1.6.14.0" creationDateTime="2022-04-15T09:10:35.3386187" />
    <contentHeader name="Krasnodar_TZiVO.project" modificationDateTime="2022-04-15T09:09:05.7816639">
    <coordinateInfo>
        <fbd>
        <scaling x="1" y="1" />
        </fbd>
        <ld>
        <scaling x="1" y="1" />
        </ld>
        <sfc>
        <scaling x="1" y="1" />
        </sfc>
    </coordinateInfo>
    <addData>
        <data name="http://www.3s-software.com/plcopenxml/projectinformation" handleUnknown="implementation">
        <ProjectInformation />
        </data>
    </addData>
    </contentHeader>
    <types>
    <dataTypes />
    <pous>
        <pou name="FB_HANDLE_ANPAR" pouType="functionBlock">
        <interface>
            <localVars>
            <variable name="PV_IN">
                <type>
                <REAL />
                </type>
            </variable>
            <variable name="CSF">
                <type>
                <BOOL />
                </type>
            </variable>
            <variable name="PV_IN_FLD">
                <type>
                <REAL />
                </type>
            </variable>
            <variable name="MODE">
                <type>
                <INT />
                </type>
            </variable>
            <variable name="T_SAMPLE">
                <type>
                <TIME />
                </type>
            </variable>			
            <variable name="STARTUP">
                <type>
                <BOOL />
                </type>
            </variable>
            <variable name="EN_IMT">
                <type>
                <BOOL />
                </type>
            </variable>
            <variable name="_real">
                <type>
                <REAL />
                </type>
            </variable>
            <variable name="_bool">
                <type>
                <BOOL />
                </type>
            </variable>
            <variable name="CHAIN">
                <type>
                <INT />
                </type>
                <initialValue>
                <simpleValue value="0" />
                </initialValue>
            </variable>
            <variable name="CHAIN_Quantity">
                <type>
                <INT />
                </type>
                <initialValue>
                <simpleValue value="10" />
                </initialValue>
                <documentation>
                <xhtml xmlns="http://www.w3.org/1999/xhtml"> Настраиваемый параметр - Количество циклов выделенных для разнесения выводов </xhtml>
                </documentation>
            </variable>
            <variable name="T_SAMPLE_CHAIN">
                <type>
                <TIME />
                </type>
            </variable>
            </localVars>
            <localVars constant="true">
            <variable name="TYPE_420">
                <type>
                <INT />
                </type>
                <initialValue>
                <simpleValue value="1" />
                </initialValue>
            </variable>
            <variable name="TYPE_020">
                <type>
                <INT />
                </type>
                <initialValue>
                <simpleValue value="2" />
                </initialValue>
            </variable>
            <variable name="TYPE_PT100">
                <type>
                <INT />
                </type>
                <initialValue>
                <simpleValue value="3" />
                </initialValue>
            </variable>
            <variable name="TYPE_50M">
                <type>
                <INT />
                </type>
                <initialValue>
                <simpleValue value="4" />
                </initialValue>
            </variable>
            <variable name="TYPE_K">
                <type>
                <INT />
                </type>
                <initialValue>
                <simpleValue value="5" />
                </initialValue>
            </variable>
            </localVars>
        </interface>
        <body>
            <ST>
            <xhtml xmlns="http://www.w3.org/1999/xhtml">STARTUP:=STARTUP_100;
EN_IMT:=EN_IMITATION;
T_SAMPLE:=T_SAMPLE_100;
T_SAMPLE_CHAIN:=T_SAMPLE * CHAIN_Quantity;

//***********Приоритет вызовов блока**************
CHAIN := CHAIN +1; // Счетчик вызовов, для разграничения вызовов блоков
IF CHAIN &gt; CHAIN_Quantity THEN CHAIN:= 1; END_IF;
//***********Приоритет вызовов блока**************
''')

f += '\n'
# Флаг имитации (Если "IMT_YES" то подвязываемся к блоку имитации, иначе заглушка)
IMT_YES = False

anpars = projectFile['AnPar'].iloc

for par in anpars:

    if par['FB'] == 'iPARAM_MON':

        f += '\n'
        f.startObject(par['OBJ_POSITION'])

        f.setTab('')
        f += ('// ' + par['KIP1'] + ' ' + ('(' + par['KIP2'] + ')','')[par['KIP2']==''] + ' - ' + projectFile['INFO_AGREGAT'] + '. ' + par['DESCRIPTION'] + ' : ' + par['FB'])

        if not par['CHAIN'] == 0:
            f += ('\n\tIF CHAIN=' + str(par['CHAIN']) + ' OR STARTUP THEN')

        modeName = ''
        if par['TYPE'] == '4-20':
            modeName = 'TYPE_420'
        elif par['TYPE'] == '0-20':
            modeName = 'TYPE_020'
        elif par['TYPE'] in ('Pt100', '100П', 'RTD'):
            modeName = 'TYPE_PT100'
        elif par['TYPE'] in ('M50', '50M', 'М50', '50М'):
            modeName = 'TYPE_50M'
        elif par['TYPE'] in ('TXA', 'ТХА', 'TC'):
            modeName = 'TYPE_K'

        f.setTab('			')        
        f += ('''
	    FC_iAI(
		    EN_IMT := EN_IMT,
''')
        f += (('IMT_PV := HANDLE_IMT.'+ par['OBJ_POSITION'] + '_PV,', 'IMT_PV := ' + str(par['LLM']))[not IMT_YES] + '\n')
        f += ('IMT_CSF := FALSE,\n')
        f += ('MODE = '+modeName+',\n')
        f += ('PV_HLM :=' + par['OBJ_POSITION'] + '.HLM,\n')
        f += ('PV_LLM :=' + par['OBJ_POSITION'] + '.LLM,\n')
        f += ('MODULE_CSF = ' + par['CHANNEL'][:-(len(par['CHANNEL'])-par['CHANNEL'].rindex('_'))] + '.HwError,\n' )
        f += ('STATUS :=' + par['OBJ_POSITION'] + '_.Status,\n')
        f += ('PV_IN :=' + par['OBJ_POSITION'] + '_.Value,')
        f += ('''
			QPV=&gt; PV_IN,
			QCSF=&gt; CSF,
			QPV_IN=&gt; PV_IN_FLD);
''')

        f.setTab('		') 
        f += (par['OBJ_POSITION']+'(\n')
        f += ('\tRED_DATA := RED.PARAMON_RED[' + str(par['RED_ID']) + '],')

        if not par['CHAIN'] == 0:
            f += '\n'
            f += ('\tT_SAMPLE := T_SAMPLE_CHAIN')

        f += ('''
  			STARTUP := STARTUP,
			CSF := CSF,
			PV_IN := PV_IN,
			PV_FLD := PV_IN_FLD);      
 ''')
        if not par['CHAIN'] == 0:
            f += ('END_IF;\n')

        f.endObject()
 
    elif par['FB'] in ('iPARAM_out', 'iPARAM_OUT'):
        pass

    elif par['FB'] in ('iPARAM_NETWORK_out', 'iPARAM_NETWORK_OUT'):
        pass

    elif par['FB'] == 'iPARAM_NETWORK':
        pass

    elif par['FB'] == 'iFLOW_GAS_Vn':
        pass

    elif par['FB'] == 'iCALC':
        pass

    elif par['FB'] == 'iLEVEL':
        pass

    elif par['FB'] in ('iFLOW_STM_V', 'iFLOW_STM_M', 'iFLOW_WAT_V', 'iFLOW_WAT_M', 'iFLOW_GAS_V', 'iFLOW_GAS_M', 'iFLOW_AIR_V', 'iFLOW_AIR_M', 'iFLOW_FUEL_V', 'iFLOW_FUEL_M'):
        pass

    elif par['FB'] == 'iDOUBLE':
        pass

    elif par['FB'] == 'iTRIPLE':
        pass

f += ('\n')

f.setNewObjectLocation()

f += ('\n')

f += ('''	
            </xhtml>
            </ST>
        </body>
        <addData>
            <data name="http://www.3s-software.com/plcopenxml/objectid" handleUnknown="discard">
            <ObjectId>b744546d-ad16-48aa-a4b7-8aee514630fd</ObjectId>
            </data>
        </addData>
        </pou>
    </pous>
    </types>
    <instances>
    <configurations />
    </instances>
    <addData>
    <data name="http://www.3s-software.com/plcopenxml/projectstructure" handleUnknown="discard">
        <ProjectStructure>
        <Object Name="FC_HANDLE_ANPAR" ObjectId="b744546d-ad16-48aa-a4b7-8aee514630fd" />
        </ProjectStructure>
    </data>
    </addData>
</project>
''')

f.close()

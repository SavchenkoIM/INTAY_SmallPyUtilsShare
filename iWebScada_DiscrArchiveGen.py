

QWORD_Num = 0
QWBIT_Num = 0

def printScript(objects: list, bits: list, template: str, prefix: str, postfix):
    global QWORD_Num
    global QWBIT_Num

    res = ''
    for obj in objects:
        for b, bit in enumerate(bits):
            if QWBIT_Num + len(bits) - b >= 64:
                QWBIT_Num = 0
                QWORD_Num += 1
            res += template.format(ObjName=obj, BitNum=bit, QWNum = QWORD_Num, QWBIT = QWBIT_Num, Prefix = prefix, Postfix = postfix)
            QWBIT_Num += 1

    return res

Tmpl = 'Monitor_State.QWORD{QWNum}.Value=Math.SetBit(Monitor_State.QWORD{QWNum}.Value,{QWBIT},Math.TestBit({Prefix}.{ObjName}.{Postfix}.STATE.Value,{BitNum}));\n'


# ====================================== DE_MON/DG_EVENT =========================================

DEMON_BitNum = ['6', '7', '30'] 
# PV, CSF, SIM
DEMON_Prefix = 'DE_MON'
DEMON_Postfix = 'DE_MON'

DEMON_KA1 = ['KA1_DE_BurnerFlame_L1B1',
        'KA1_DE_BurnerFlame_L1B2',
        'KA1_DE_BurnerFlame_L1B3',
        'KA1_DE_BurnerFlame_L1B4',
        'KA1_DE_BurnerFlame_L2B1',
        'KA1_DE_BurnerFlame_L2B2',
        'KA1_DE_BurnerFlame_L2B3',
        'KA1_DE_BurnerFlame_L2B4',
        'KA1_DE_BurnerFlame_L3B1',
        'KA1_DE_BurnerFlame_L3B2',
        'KA1_DE_BurnerFlame_L3B3',
        'KA1_DE_BurnerFlame_L3B4',
        'KA1_DE1_NoFlame_FurnaceFD1',
        'KA1_DE2_NoFlame_FurnaceFD1',
        'KA1_DE2_NoFlame_FurnaceFD1',
        'KA1_DE2_NoFlame_FurnaceFD2',
        'KA1_DE_FaultFurnaceFD1',
        'KA1_DE_FaultFurnaceFD2',
        'KA1_DE_BurnerFlame_Cmn']



# ====================================== PARAM/DOUBLE/TRIPLE =========================================

PARAM_BitNum = ['0', '5', '1', '4', '30', '6']  
# AL, AH, WL, WH, SIM, CSF
PARAM_Prefix='PARAM_MON'
PARAM_Postfix='PARAM_MON'

PARAM_KA1 = ['KA1_ABR_Furnace_p1',
        'KA1_ABR_Furnace_p2',
        'KA1_AFM_FeedWaAftPVD',
        'KA1_AFM_HPStmAftBoiler_F1',
        'KA1_AFM_HPStmAftBoiler_F2',
        'KA1_AFM_HPStmAftBoiler_F2_1',
        'KA1_AL_WaInBVD',
        'KA1_AP_HPStmInBVD',
        'KA1_AP_mFeedWaAftPVD',
        'KA1_AP_Mix',
        'KA1_AP_SmokeTopFurnace',
        'KA1_AT_FeedWaBefBoiler']

PARAM_PTU1 = ['ECHSRZ1_AF_Grid',
        'ECHSRZ1_AFR_Turb',
        'ECHSRZ1_AG_RKCSD1',
        'ECHSRZ1_AG_RKCSD2',
        'ECHSRZ1_AG_RKCVD1',
        'ECHSRZ1_AG_RKCVD2',
        'ECHSRZ1_AN_Gen',
        'ECHSRZ1_AT_NWaBefPSG',
        'TZiVO1_AFM_CondToRegen',
        'TZiVO1_AG_StmRKPO',
        'TZiVO1_AL_CondInBotCTank',
        'TZiVO1_AL_CondInCTank',
        'TZiVO1_AP_CondAftKEN',
        'TZiVO1_AP_mCondToRegen',
        'TZiVO1_AP_StmInCond',
        'TZiVO1_AT_mCondToRegen',
        'TZiVO1_AG_CondToDrt']

PARAM_OSO1 = ['PPVK1_AFM_CondBefPND',
        'PPVK1_AFM_StmBefBROU1',
        'PPVK1_AG_StmBefBROU1',
        'PPVK1_AG_StmBefBROU2A',
        'PPVK1_AG_StmBefBROU2B',
        'PPVK1_AL_CondInPND1',
        'PPVK1_AL_CondInPND2',
        'PPVK1_AL_CondInPND3',
        'PPVK1_AL_CondInPPSV',
        'PPVK1_AL_CondInPSV21',
        'PPVK1_AL_CondInPSV22',
        'PPVK1_AL_CondInPVD4',
        'PPVK1_AL_CondInPVD5',
        'PPVK1_AL_CondInPVD6',
        'PPVK1_AL_CondInSKG',
        'PPVK1_AL_WatInDea',
        'PPVK1_AP_AirNgFans',
        'PPVK1_AP_CondBefPND',
        'PPVK1_AP_FNWaFrHeats',
        'PPVK1_AP_LPStmFrBoiler_F1',
        'PPVK1_AP_LPStmFrBoiler_F2',
        'PPVK1_AP_RNWatBefGrPSG',
        'PPVK1_AP_StmAirInDea',
        'PPVK1_AP_WatBefPVD',
        'PPVK1_AT_CondBefPND',
        'PPVK1_AT_FNWaFrHeats',
        'PPVK1_AT_StmInPipeAftBRL_F1',
        'PPVK1_AT_StmInPipeAftBRL_F2',
        'PPVK1_AT_WatAftGrPVD',
        'PPVK1_AT_WatBefPVD']


# ====================================== VALVE =========================================

VALVE_BitNum = ['0', '3', '1', '4', '8', '24', '23', '22', '21', '18', '30', '25']  
# OPEN, OPENINIG, CLOSE, CLOSING, CSF, EF, QAUTO, QMAN, QLOCAL, QBL, QSIM, QREP
VALVE_Prefix='VALVE'
VALVE_Postfix='VALVE_ST'

VALVE_KA1 = ['KA1_VC_FeedWaBefECO_L1',
        'KA1_VC_FeedWaBefECO_L2',
        'KA1_VC_FeedWaBypBefECO_L1',
        'KA1_VC_FeedWaBypBefECO_L2',
        'KA1_VS_FeedWaBefECO_L1',
        'KA1_VS_FeedWaBefECO_L2',
        'KA1_VS_FeedWaBypBefECO_L1',
        'KA1_VS_FeedWaBypBefECO_L2',
        'KA1_VS_StmAftBoiler_F1',
        'KA1_VS_StmAftBoiler_F2',
        'KA1_VS_WaCircBVDtoECO']

VALVE_PTU1 = ['TZiVO1_VC_CondRecirCTank',
        'TZiVO1_VC_CondToDrt',
        'TZiVO1_VS_BypCondRecirCTank',
        'TZiVO1_VS_BypCondToDrt',
        'TZiVO1_VS_GPZ_F1',
        'TZiVO1_VS_GPZ_F2',
        'TZiVO1_VS_LPStmToBoiler_F1',
        'TZiVO1_VS_LPStmToBoiler_F2',
        'TZiVO1_VS_NgKEN1',
        'TZiVO1_VS_NgKEN2',
        'TZiVO1_VS_StmPO',
        'TZiVO1_VS1_LPStmToPlant',
        'TZiVO1_VS2_LPStmToPlant',
        'TZiVO1_VX_KOS1',
        'TZiVO1_VX_KOS2',
        'TZiVO1_VX_KOS3',
        'TZiVO1_VX_KOS4',
        'TZiVO1_VX_KOS5',
        'TZiVO1_VX_KOS6',
        'TZiVO1_VX_KOS7']

VALVE_OSO1 = ['PPVK1_VC_FNWaAftHeats',
        'PPVK1_VC_FNWaBefPSV',
        'PPVK1_VC_FNWaBypHeats',
        'PPVK1_VC_FNWaBypPPSV',
        'PPVK1_VC_RNWaBypPSG',
        'PPVK1_VC_StmBefBROU1',
        'PPVK1_VC_StmBefBROU2A',
        'PPVK1_VC_StmBefBROU2B',
        'PPVK1_VC_StmToDea',
        'PPVK1_VC_StmToPPSV',
        'PPVK1_VS_FNWaAftPSV21',
        'PPVK1_VS_FNWaAftPSV22',
        'PPVK1_VS_FNWaBefPPSV',
        'PPVK1_VS_FNWaBefPSV21',
        'PPVK1_VS_FNWaBefPSV22',
        'PPVK1_VS_NgPEN1A',
        'PPVK1_VS_NgPEN1B',
        'PPVK1_VS_RNWaBefHeats',
        'PPVK1_VS_StmBefBROU1',
        'PPVK1_VS_StmBefBROU2A',
        'PPVK1_VS_StmBefBROU2B',
        'PPVK1_VS_StmFrPVD4ToDea',
        'PPVK1_VS_StmToDea',
        'PPVK1_VS_StmToPND1',
        'PPVK1_VS_StmToPND2',
        'PPVK1_VS_StmToPND3',
        'PPVK1_VS_StmToPSV21',
        'PPVK1_VS_StmToPSV22',
        'PPVK1_VS_StmToPVD4',
        'PPVK1_VS_StmToPVD5',
        'PPVK1_VS_StmToPVD6',
        'PPVK1_VS_VsPEN1A',
        'PPVK1_VS_VsPEN1B',
        'PPVK1_VS_WatBypPVD',
        'PPVK1_VS1_WatAftGrPVD',
        'PPVK1_VS1_WatBefGrPVD']





with open('D:\script_KA1.txt', mode='wt+', encoding='utf-8') as f:
    f.write('// ================ KA1 ===========================\n')
    f.write('// DEMON/DGEVENT\n')
    f.write(printScript(DEMON_KA1, DEMON_BitNum, Tmpl, DEMON_Prefix, DEMON_Postfix))
    f.write('// PARAM/DOUBLE/TRIPLE\n')
    f.write(printScript(PARAM_KA1, PARAM_BitNum, Tmpl, PARAM_Prefix, PARAM_Postfix))
    f.write('// VALVE\n')
    f.write(printScript(VALVE_KA1, VALVE_BitNum, Tmpl, VALVE_Prefix, VALVE_Postfix))
QWORD_Num += 1
QWBIT_Num = 0

with open('D:\script_PTU1.txt', mode='wt+', encoding='utf-8') as f:
    f.write('// ================ PTU1 ===========================\n')
    f.write('// PARAM/DOUBLE/TRIPLE\n')
    f.write(printScript(PARAM_PTU1, PARAM_BitNum, Tmpl, PARAM_Prefix, PARAM_Postfix))
    f.write('// VALVE\n')
    f.write(printScript(VALVE_PTU1, VALVE_BitNum, Tmpl, VALVE_Prefix, VALVE_Postfix))

QWORD_Num += 1
QWBIT_Num = 0

with open('D:\script_OSO1.txt', mode='wt+', encoding='utf-8') as f:
    f.write('// ================ OSO1 ===========================\n')
    f.write('// PARAM/DOUBLE/TRIPLE\n')
    f.write(printScript(PARAM_OSO1, PARAM_BitNum, Tmpl, PARAM_Prefix, PARAM_Postfix))
    f.write('// VALVE\n')
    f.write(printScript(VALVE_OSO1, VALVE_BitNum, Tmpl, VALVE_Prefix, VALVE_Postfix))
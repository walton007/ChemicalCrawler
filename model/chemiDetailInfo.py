class ChemicalProperty(object):
    def __init__(self, rongdian, feidian, shandian, CASLink, NISTChemicalLink, EPAChemicalLink):
        self.rongdian = rongdian
        self.feidian = feidian
        self.shandian = shandian
        self.CASLink = CASLink
        self.NISTChemicalLink = NISTChemicalLink
        self.EPAChemicalLink = EPAChemicalLink

class ChemicalSecurityInfo(object):
    def __init__(self, securityLevelLink, securityNoteLink, transferID):
        self.securityLevelLink = securityLevelLink
        self.securityNoteLink = securityNoteLink
        self.transferID = transferID


class ChemiDetailInfo(object):
    def __init__(self, CAS, enName, enSynonym, zhName, zhSynonym, CBNumber, formula , molecular ,
        mofile, chemicalProperty, securityInfo):
        self.CAS = CAS
        self.enName = enName
        self.enSynonym = enSynonym
        self.zhName = zhName
        self.zhSynonym = zhSynonym
        self.CBNumber = CBNumber
        self.molecular = molecular
        self.formula = formula
        self.mofile = mofile
        self.chemicalProperty = chemicalProperty

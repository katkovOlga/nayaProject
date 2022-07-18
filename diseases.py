class Diseases(object):
    def __init__(self,
                 debug_flg,       #1
                 id,              #2
                 name,            #3
                 effective_date,  #4
                 expiration_date  ): # 5
        self.id              = id,
        self.name            = name,
        self.effective_date  = effective_date,
        self.expiration_date = expiration_date

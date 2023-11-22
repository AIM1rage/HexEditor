

def parse_buffer(buffer: str):
    alphabet = "0123456789abcdef"
    res = []
    
    
    for x in buffer:
        if x in alphabet:
            res.append(x)
    
    

    return 
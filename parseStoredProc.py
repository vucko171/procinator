import re, pyperclip, time
def parse(data):
    data=data.split("\n")
    name=""
    ret=""
    err_code=False
    params=[]
    for line in data:
        if name=="":
            nameArr = re.findall(r'\.CommandText\s*=\s*".*?JAGORA\.(.*?)(?:"|\()',line,flags=re.I)
            if len(nameArr):
                name=nameArr[0]
        paramsArr=re.findall(r'\.CreateParameter\((.*?),.*adParamInput.*?,.*?,(.*?)\)\s*$', line, flags=re.I)
        if "p_err_code" in line.lower():
            err_code=True
        if len(paramsArr):
            params.append(paramsArr[0])
    ret+="try {\n"
    ret+="  const sp = new CallStoredProcedure(connection);\n"
    ret+="  sp.commandText = 'JAGORA."+name+"';\n"
    for param in params:
        ret+="  sp.createParameter("+param[0]+", "+param[1]+");\n"
    ret+="  const temp = await sp.execute(false);\n"
    if err_code:
        ret+='''  if (temp.P_ERR_CODE) {
   const errorObj = new SRTError(
     ` Error occurred calling Stored Procedure(JAGORA.'''+name+'''): ${temp.P_ERR_MSG}`,
     '',
     temp.P_ERR_CODE.toString(),
     '',
     temp.P_ERR_MSG,
     '',
     '',
     ''
   );
   errorObj.printSRTErrorToConsole();
   throw errorObj;
  }\n'''
    ret+="} catch (error) {\n"
    ret+="  connection.rollback();\n"
    ret+="  throw new Error(error);\n"
    ret+="  // do something\n"
    ret+="}\n"
    print(params)
    return ret

    
if __name__=="__main__":
    ptext=""
    while(1):
        text=pyperclip.paste()
        if text!=ptext:
            if "CommandText" in text:
                ret=parse(text)
                pyperclip.copy(ret)
                text=ret
            ptext=text
        time.sleep(0.1)


function HCF(u, v) { 
    var U = u, V = v
    while (true) {
        if (!(U%=V)) return V
        if (!(V%=U)) return U 
    } 
}
//convert a decimal into a fraction
function fraction(decimalF){
    if(!decimalF){
        decimalF=this;
    }
    whole = String(decimalF).split('.')[0];
    decimalF = parseFloat("."+String(decimalF).split('.')[1]);
    num = "1";
    for(z=0; z<String(decimalF).length-2; z++){
        num += "0";
    }
    decimalF = decimalF*num;
    num = parseInt(num);
    for(z=2; z<decimalF+1; z++){
        if(decimalF%z==0 && num%z==0){
            decimalF = decimalF/z;
            num = num/z;
            z=2;
        }
    }


    //if format of fraction is xx/xxx
    if (decimalF.toString().length == 2 && 
            num.toString().length == 3) {
                //reduce by removing trailing 0's
        decimalF = Math.round(Math.round(decimalF)/10);
        num = Math.round(Math.round(num)/10);
    }
    //if format of fraction is xx/xx
    else if (decimalF.toString().length == 2 && 
            num.toString().length == 2) {
        decimalF = Math.round(decimalF/10);
        num = Math.round(num/10);
    }
    //get highest common factor to simplify
    var t = HCF(decimalF, num);
    if (isNaN(decimalF) == true){
        return ((whole==0)?"" : whole+" ")
    } else {
        //return the fraction after simplifying it
        return ((whole==0)?"" : whole+" ")+decimalF/t+"/"+num/t;
    }
    
}



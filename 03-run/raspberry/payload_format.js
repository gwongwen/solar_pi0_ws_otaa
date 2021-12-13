function Decoder(bytes, port) {
    var decoded = {};
    decoded.Pressure = ((bytes[0] << 8) | bytes[1])/100
    if(bytes[2] === 0){
        decoded.Temperature = ((bytes[3] << 8) | bytes[4])/100
    }else{
        decoded.Temperature = (((bytes[3] << 8)| bytes[4]) * -1)/100
    }
 
    return decoded;
  }

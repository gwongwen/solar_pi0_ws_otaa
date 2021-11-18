function Decoder(bytes, port) {
    var decoded = {};
    decoded.Pressure = ((bytes[0] << 16) | (bytes[1] << 8) | bytes[2])/100
    if(bytes[3] == 0){
        decoded.Temperature = ((bytes[4] << 8) | bytes[5])/100
    }else{
        decoded.Temperature = (((bytes[4] << 8)| bytes[5]) * -1)/100
    }
    decoded.Altitude = ((bytes[11] << 16) | (bytes[12] << 8) | bytes[13])/100

    return decoded;
  }

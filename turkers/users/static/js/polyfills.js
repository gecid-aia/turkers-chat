const objectToValuesPolyfill = function(object){
  return Object.keys(object).map(function(key){ return object[key]});
};
Object.values = Object.values || objectToValuesPolyfill;

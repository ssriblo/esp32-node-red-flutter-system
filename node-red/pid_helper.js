// ~/.node-red/pid_helper.js

module.exports = {
  init: function(ctx) {
    ctx.lastTime = Date.now();
    ctx.lastError = 0;
    ctx.integral = 0;
    ctx.kp = 2.5;
    ctx.ki = 0.1;
    ctx.kd = 0.5;
  },

  compute: function(ctx, processValue, setpoint) {
    var now = Date.now();
    var dt = (now - ctx.lastTime) / 1000;
    ctx.lastTime = now;

    if (typeof processValue === 'undefined') {
      console.warn('PID compute skipped — processValue is undefined');
      return { output: 0, p: 0, i: 0, d: 0 };
    }

    if (dt <= 0) {
      console.warn('PID compute skipped — dt non-positive:', dt);
      return { output: 0, p: 0, i: 0, d: 0 };
    }

    var error = setpoint - processValue;
    var P = ctx.kp * error;
    ctx.integral += error * dt;
    var I = ctx.ki * ctx.integral;
    var D = ctx.kd * ((error - ctx.lastError) / dt);
    ctx.lastError = error;

    var output = P + I + D;
    output = Math.max(0, Math.min(100, output));

    return { output: output, p: P, i: I, d: D };
  }

};

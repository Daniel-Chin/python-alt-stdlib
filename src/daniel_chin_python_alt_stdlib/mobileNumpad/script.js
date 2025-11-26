const state = {
  started: false, 
  start_pos: null, 
  canceling: false, 
  now_pos: null,
  num_touches: 0,
  last_action: null,
};

const touchStart = (event) => {
  state.num_touches ++;
  if (state.started) {
    if (state.num_touches == 1) console.error('vtw4n7c');
    state.canceling = true;
  } else {
    if (state.num_touches != 1) console.error('erwo873gh4');
    state.started = true;
    state.canceling = false;
    state.start_pos = event.targetTouches[0];
    state.now_pos = state.start_pos;
  }
  should_draw = true;
};

const touchMove = (event) => {
  if (! state.canceling) {
    if (! state.started) console.error('74g5wh');
    state.now_pos = event.targetTouches[0];
  }
  should_draw = true;
};

const touchEnd = (_) => {
  state.num_touches --;
  if (! state.canceling) {
    onSwipe();
  }
  if (state.num_touches == 0) {
    state.started = false;
  }
  should_draw = true;
};

const touchCancel = (_) => {
  state.num_touches --;
  if (state.num_touches == 0) {
    state.started = false;
  }
  should_draw = true;
};

const onSwipe = () => {
  const intent = parseIntent();
  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", intent, true);
  xhttp.send();
  state.last_action = intent;
};

const sqr2 = .5 **.5;
const LOOKUP = [
  { ref: [1    , 0    ], num: 6 }, 
  { ref: [sqr2 , sqr2 ], num: 9 }, 
  { ref: [0    , 1    ], num: 8 }, 
  { ref: [-sqr2, sqr2 ], num: 7 }, 
  { ref: [-1   , 0    ], num: 4 }, 
  { ref: [-sqr2, -sqr2], num: 1 }, 
  { ref: [0    , -1   ], num: 2 }, 
  { ref: [sqr2 , -sqr2], num: 3 }, 
];
const DOT_PRODUCT_THRESHOLD = Math.cos(Math.PI * .125);
const parseIntent = () => {
  let x = state.now_pos.pageX - state.start_pos.pageX;
  let y = state.now_pos.pageY - state.start_pos.pageY;
  const magnitude = (x**2 + y**2) ** .5;
  const threshold = window.innerWidth * .05;
  if (magnitude < threshold) {
    return 5;
  }
  x /= magnitude; // normalize
  y /= magnitude;
  return LOOKUP.filter(({ ref }) => (
    ref[0] * x - ref[1] * y >= DOT_PRODUCT_THRESHOLD * .99
  ))[0].num;
};

const FPS = 60;
const tick = (main) => {
  setTimeout(() => {
    draw(main);
    requestAnimationFrame(tick.bind(null, main));
  }, 1000 / FPS);
};

let should_draw = true;
const draw = (main) => {
  if (should_draw) {
    should_draw = false;  // Race Condition?
    if (state.started) {
      if (state.canceling) {
        main.innerHTML = 'Multiple fingers detected. <br/> Canceling!';
      } else {
        const intent = parseIntent();
        main.innerHTML = `Release to send <br/>"${intent}"`;
      }
    } else {
      if (state.last_action) {
        main.innerHTML = `Sent "${state.last_action}". `;
      } else {
        main.innerHTML = 'Swipe anywhere. ';
      }
    }
  }
};

window.onload = () => {
  const main = document.getElementById('main');
  main.addEventListener('touchstart', touchStart);
  main.addEventListener('touchmove', touchMove);
  main.addEventListener('touchend', touchEnd);
  main.addEventListener('touchcancel', touchCancel);
  tick(main);
};

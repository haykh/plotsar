window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache: 'global'
  }
};

(function () {
  var script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
  script.async = true;
  document.head.appendChild(script);
})();

setTimeout(() => {
  plot = document.getElementsByClassName('js-plotly-plot')[0];
  plot.onclick = () => {
    for (let i = 0; i < 10; i++) {
      setTimeout(() => {
        MathJax.startup.promise.then(() => {
          MathJax.typesetPromise()
        });
      }, 10 * i);
    }
  };
}, 1000);
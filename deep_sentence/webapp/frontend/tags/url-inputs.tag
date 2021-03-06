require('./url-input.tag');

<url-inputs>
  <url-input
    each={ url, i in opts.urls }
    url={ url }
    onadd={ parent.addURL }
    onremove={ parent.removeURL }
    index={ i + 1 }
    show-delete={ i !== 0 }
    show-add-url={ i === parent.opts.urls.length - 1 && i < 2 } />

  <script>
    this.addURL = () => {
      opts.urls.push({value: ''});
      this.update();
    };

    this.removeURL = (e) => {
      opts.urls.splice(e.item.i, 1);
      this.update();
    }
  </script>
</url-inputs>

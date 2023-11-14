---
layout: default
permalink: /tags/
title: Tags
---

<section class="content">
{% assign tag_list = site.tags | sort %}
{% for tag in tag_list %}
  <div class="tag-group" id="#{{ tag_name | slugize }}">
    {% capture tag_name %}{{ tag | first }}{% endcapture %}
    <h2>{{ tag_name }}</h2>
    <ul>
    {% for post in site.tags[tag_name] %}
    <li>
      <a href="{{ site.baseurl }}{{ post.url }}">{{ post.date | date: "%Y-%m-%d" }} - {{post.title}}</a>
    </li>
    {% endfor %}
    </ul>
  </div>
{% endfor %}
</section>
---
layout: default
permalink: /index/
title: Index
---

<section class="content">
{% assign posts_by_month = site.posts | group_by_exp: "item", "item.date | date: '%b %Y'" %}
{% for group in posts_by_month %}
<h2>{{ group.name }}</h2>
<ul>
  {% for post in group.items %}
    <li>
      <a href="{{ site.baseurl }}{{ post.url }}">{{ post.date | date: "%Y-%m-%d" }} - {{post.title}}</a>
    </li>
  {% endfor %}
</ul>
{% endfor %}
</section>
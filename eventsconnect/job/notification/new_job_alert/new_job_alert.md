Hey,

A new EventJob Opportunity has been created. 

<p>Company Name: {{ doc.company_name}}</p>
<p>EventJob Title: {{ doc.eventjob_title}}</p>
<p>EventJob Location: {{ doc.location}}</p><br>
<p>EventJob Description: {{ doc.description}}</p><br>

<p>Find all the posted eventjobs  <a href="{{ frappe.utils.get_url() }}/app/eventjob-opportunity">here</a>.</p><br>

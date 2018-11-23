package com.glarimy.cities;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.UriComponentsBuilder;

@RestController
@RequestMapping(path = "/city")
public class CityController {
	@Autowired
	private CityService service;

	@RequestMapping(path = "/{id}", produces = { "application/xml", "application/json" })
	public ResponseEntity<City> find(@PathVariable("id") String id) {
		City city = service.find(id);
		return new ResponseEntity<City>(city, HttpStatus.OK);
	}

	@RequestMapping(path = "/", produces = { "application/xml", "application/json" })
	public ResponseEntity<List<City>> search(@RequestParam(value = "name", required = false) String name) {
		List<City> cities;
		if (name == null)
			cities = service.list();
		else
			cities = service.search(name);
		return new ResponseEntity<List<City>>(cities, HttpStatus.OK);
	}

	@RequestMapping(path = "/", method = RequestMethod.POST)
	public ResponseEntity<City> add(@RequestBody City city, UriComponentsBuilder builder) {
		city = service.save(city);
		HttpHeaders headers = new HttpHeaders();
		headers.setLocation(builder.path("/city/{id}").buildAndExpand(city.getId()).toUri());
		return new ResponseEntity<City>(city, headers, HttpStatus.CREATED);
	}
}
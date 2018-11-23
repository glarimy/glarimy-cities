package com.glarimy.cities;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CityService {
	@Autowired
	private CityRepository repo;

	public City find(String id) throws CityNotFoundException {
		return repo.findById(id).orElseThrow(() -> new CityNotFoundException());
	}

	public List<City> search(String name) {
		return repo.findByNameLike(name);
	}

	public List<City> list() {
		return repo.findAll();
	}

	public City save(City city) {
		return repo.save(city);
	}
}

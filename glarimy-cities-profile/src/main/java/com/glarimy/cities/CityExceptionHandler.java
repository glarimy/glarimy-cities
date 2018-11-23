package com.glarimy.cities;

import javax.validation.ConstraintViolationException;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

@ControllerAdvice
@RestController
public class CityExceptionHandler extends ResponseEntityExceptionHandler {

	@ExceptionHandler(Throwable.class)
	public final ResponseEntity<CityError> handleException(Throwable t, WebRequest request) {
		if (t instanceof ConstraintViolationException) {
			CityError error = new CityError();
			error.setMessage(t.getMessage());
			return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
		}
		if (t instanceof CityNotFoundException)
			return new ResponseEntity<>(HttpStatus.NOT_FOUND);
		return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
	}
}

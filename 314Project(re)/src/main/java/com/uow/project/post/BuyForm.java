package com.uow.project.post;


import org.springframework.web.bind.annotation.RequestParam;

import com.uow.project.post.field.FloorLevel;
import com.uow.project.post.field.Furnishing;
import com.uow.project.post.field.PropertyType;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class BuyForm {
	@NotNull(message = "Subject is a mandatory component.")
	@Size(max = 50)
	private String subject;

	//content는 선택
	@Size(max = 500)
	private String content;
	
	@NotNull(message = "Address is a mandatory component.")
	private String address;
	
	
	@NotNull(message = "Property type is a mandatory component.")
	private PropertyType propertyType;
	
	@NotNull(message = "Floor size is a mandatory component.")
	private int floorsize;
	
	@NotNull(message = "Furnishing is a mandatory component.")
	private Furnishing furnishing;
	
	@NotNull(message = "Floor level is a mandatory component.")
	private FloorLevel floorlevel;
	
	@NotNull(message = "Built year is a mandatory component.")
	private int top;
	
	@NotNull(message = "Price is a mandatory component.")
	private int price;
	
}
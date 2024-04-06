package com.example.demo;

import lombok.Getter;
import lombok.RequiredArgsConstructor; 

@RequiredArgsConstructor
@Getter
public class DemoLombok {
    private final String hello;
    private final int lombok;
    
    public static void main(String[] args) {
        DemoLombok demoLombok = new DemoLombok("데모",5);

        System.out.println(demoLombok.getHello());
        System.out.println(demoLombok.getLombok());
    }
}

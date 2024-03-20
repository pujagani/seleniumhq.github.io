package dev.selenium.additionalcommands;

import org.checkerframework.checker.units.qual.C;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.remote.AdditionalHttpCommands;

import java.util.ServiceLoader;

class AdditionalCommandsTest {

    @Test
    void canAccessAdditionalCommands() {
    CheeseDriver driver = new  CheeseDriver(new ChromeOptions());

        ServiceLoader<AdditionalHttpCommands> loader = ServiceLoader.load(AdditionalHttpCommands.class);
        loader.forEach(l -> System.out.println(l.getClass()));
        String result = driver.getCheese();
    }
}

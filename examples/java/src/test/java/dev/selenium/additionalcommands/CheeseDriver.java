package dev.selenium.additionalcommands;

import org.openqa.selenium.Capabilities;
import org.openqa.selenium.remote.HttpCommandExecutor;
import org.openqa.selenium.remote.RemoteWebDriver;

import java.util.Collections;
import java.util.Map;

public class CheeseDriver extends RemoteWebDriver {

    public CheeseDriver(Capabilities capabilities) {
    super(capabilities);
    }

    public String getCheese() {
        return (String) getExecuteMethod().execute("cheese", Collections.EMPTY_MAP);
    }
}

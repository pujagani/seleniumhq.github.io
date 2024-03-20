package dev.selenium.additionalcommands;

import com.google.auto.service.AutoService;
import com.google.common.collect.ImmutableMap;
import java.util.Map;
import org.openqa.selenium.remote.AdditionalHttpCommands;
import org.openqa.selenium.remote.CommandInfo;
import org.openqa.selenium.remote.http.HttpMethod;

@AutoService(AdditionalHttpCommands.class)
public class AddHasCheese implements AdditionalHttpCommands {
  @Override
  public Map<String, CommandInfo> getAdditionalCommands() {
    CommandInfo cheese = new CommandInfo("session/:sessionId/cheese", HttpMethod.GET);
    return ImmutableMap.of("getCheese", cheese);
  }
}

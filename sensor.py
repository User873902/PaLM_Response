from google.api_core.exceptions import ClientError
import google.generativeai as palm
from google.generativeai.types.discuss_types import ChatResponse
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_API_KEY, CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.core import callback

DEFAULT_NAME = "palm_response"
CONF_CHAT_MODEL = "model"
DEFAULT_CHAT_MODEL = "models/chat-bison-001"
CONF_TEMPERATURE = "temperature"
DEFAULT_TEMPERATURE = 0.25
CONF_TOP_P = "top_p"
DEFAULT_TOP_P = 0.95
CONF_TOP_K = "top_k"
DEFAULT_TOP_K = 40

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_CHAT_MODEL, default=DEFAULT_CHAT_MODEL): cv.string,
        vol.Optional(CONF_TEMPERATURE, default=DEFAULT_TEMPERATURE): cv.string,
        vol.Optional(CONF_TOP_P, default=DEFAULT_TOP_P): cv.string,
        vol.Optional(CONF_TOP_K, default=DEFAULT_TOP_K): cv.string,
   }
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    api_key = config[CONF_API_KEY]
    name = config[CONF_NAME]
    model = config[CONF_CHAT_MODEL]
#    temperature = config[CONF_TEMPERATURE]
#    top_p = config[CONF_TOP_P]
#    top_k = config[CONF_TOP_K]

    palm.configure(api_key=config[CONF_API_KEY])

    async_add_entities([PalmResponseSensor(hass, name, model)], True)

def generate_palm_response_sync(model, prompt, temperature, top_p, top_k):
    return palm.chat_async(
        model=model,
        prompt=prompt,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
    )

class PalmResponseSensor(SensorEntity):
  def __init__(self, hass, name, model):
    self._hass = hass
    self._name = name
    self._model = model
    self._state = None
    self._chat_response = ""

  @property
  def name(self):
    return self._name

  @property
  def state(self):
    return self._state

  @property
  def extra_state_attributes(self):
    return {"chat_response": self._chat_response}

  async def async_generate_palm_response(self, entity_id, old_state, new_state):
    new_text = new_state.state
    if new_text:
      response = await self._hass.async_add_executor_job(
        generate_palm_response_sync,
        self._model,
        new_text,
        0.25,
        0.95,
        40,
      )
      self._chat_response = chat_response.last
      self._state = "response_received"
      self.async_write_ha_state()

  async def async_added_to_hass(self):
    self.async_on_remove(
      self._hass.helpers.event.async_track_state_change(
        "input_text.palm_input", self.async_generate_palm_response
      )
    )

  async def async_update(self):
    pass

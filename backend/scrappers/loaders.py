from itemloaders.processors import TakeFirst, Identity, Compose
from itemloaders import ItemLoader
from itemadapter import ItemAdapter

from urllib import parse


def get_sub_and_main_category(value):
    data = value[0].split("/")
    main, sub = data[0], data[1]
    return [main, sub]


class JumiaUpdateItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    reveiws_out = Identity()


class JumiaProductItemLoader(ItemLoader):
    """
    Hook into the loaditem methods and prefill
    product's serch url field
    """

    default_output_processor = TakeFirst()
    name_in = Compose(lambda v: v[0], str.title)
    brand_in = Compose(TakeFirst(), str.title)

    def load_item(self):
        """
        Populate the item with the data collected so far, and return it. The
        data collected is first passed through the :ref:`output processors
        <processors>` to get the final value to assign to each item field.
        """
        adapter = ItemAdapter(self.item)
        for field_name in tuple(self._values):
            if field_name == "search_url":
                continue
            value = self.get_output_value(field_name)
            if value is not None:
                adapter[field_name] = value

        brand_param = parse.quote_plus(adapter["brand"].lower())
        name_param = parse.quote_plus(adapter["name"].lower())
        search_params = f"/{brand_param}/{name_param}/"
        adapter["search_url"] = parse.urljoin("https://www.jumia.com.ng", search_params)
        product_url = parse.quote_plus(adapter["product_url"])
        product_url = parse.urljoin("https://www.jumia.com.ng", product_url)
        adapter["product_url"] = product_url

        return adapter.item

    def url_format(x):
        return x.strip().lower().replace(" ", "+")


class ScrapperItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

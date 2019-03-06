if(len(selectors)!=0):
                for sel in selectors:
                    try:
                        data = QueensCzLvItem()
                        data["url"] = sel.xpath('a/@href').extract()[0]
                        data['website_id'] = '5bf39a8bc9a7f60004dd8d04'
                        data['sku'] = data["url"].split('/')[4]#+data["url"].split('/')[5]
                        data['name'] = sel.xpath('a/text()').extract()[0]
                        data["lv_url"] = str(response.request.url)
                        # print(data['name'])
                        # # data['media'] = get_media(div)
                        # data['brand'] = {"name":""+sel.xpath('div/a/div/div/div/div[1]/text()').extract()[0].lower(), "sub_brand":""}
                        # # data['meta'] = get_meta(div)
                        try:
                            data['price'] = self.get_price(sel)
                        except Exception as e:
                            pass

                        data['units'], data["sizes"] = self.get_units_sizes(sel)
                        yields.append(data)
                    except IndexError as ie:
                        pass
                    except Exception as e:
                        raise


                # print("*********************************************")
                # print(len(yields))
                # print("*********************************************")
                current_request_url = response.request.url
                current_offset = int(current_request_url.split('/')[-1])
                next_offset = current_offset + 1
                next_req_url = current_request_url.replace(str(current_offset),str(next_offset))
                next_req = Request(next_req_url, callback=self.parse)
                yields.append(next_req)
            return yields

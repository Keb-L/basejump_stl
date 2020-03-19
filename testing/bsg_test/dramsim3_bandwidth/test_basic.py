from trace_gen_base import TraceGenBase

class TestBasic(TraceGenBase):

  def generate(self):
    self.send_write(self.get_ch_addr(0,0,0,0))
    self.wait(1000)
    self.send_read(self.get_ch_addr(0,0,0,0))
  
    self.done()



# main()
if __name__ == "__main__":
  tg = TestBasic()
  tg.generate()


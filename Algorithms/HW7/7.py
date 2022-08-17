#    def find(self,string):
#        a = len(self.value)
#        if self.value == string[0:a]:
#            if self.value == string:
#                node = ch
#            ch = self.child
#        else:
#            return None
#
#        string = string[a:]
#        while len(string) > 0:
#            done = 0
#            while ch is not None and done == 0:
#                a = len(ch.value)
#                if ch.value == string[0:a]:
#                    if ch.value == string:
#                        node = ch
#                        string = string[a:]
#                        break
#                    ch = ch.child
#                    string = string[a:]
#                else:
#                    ch = ch.sibiling
#        return node
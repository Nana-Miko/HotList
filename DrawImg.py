from datetime import datetime
from PIL import Image, ImageDraw, ImageFont




def str_split(str):
    if len(str)<=19:
        return [str]
    else:
        split_list=[]
        for i in range(len(str)//19):
            split_list.append(str[19*i:19*(i+1)])
        if len(str)%19 !=0:
            last=str[19*(len(str)//19):]
            split_list.append(last)
        return split_list



def draw_img(source,content_list,edge=20*2,num=10):
    image_path = 'shade.png'

    im = Image.open(image_path)

    draw = ImageDraw.Draw(im)
    font_title = ImageFont.truetype(font='上首润黑体.ttf',size=39*2,encoding='utf-8')
    font_hot = ImageFont.truetype(font='榜书字体2.ttf',size=20*2,encoding='utf-8')
    draw.text((20*2,15*2),'{}热榜'.format(source),font=font_title,fill=(0,0,0))

    x=20*2
    y=90*2
    for i in range(1,num+1):
        try:
            split_list = str_split(content_list[i-1])
        except IndexError:
            break

        y_jug = y+draw.textsize('\n'.join(split_list),font=font_hot)[1]

        if y_jug>450*2:
            #print(y_jug)
            break
        if i<=3:
            draw.text((x,y),str(i)+'. ',font=font_hot,fill=(255,0,0))
        else:
            draw.text((x,y),str(i)+'. ',font=font_hot,fill=(0,0,0))
        draw.text((x+30*2,y),'\n'.join(split_list),font=font_hot,fill=(0,0,0))
        y = y_jug
        

        y=y+edge


    #im.show()
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M 查询')
    font_under = ImageFont.truetype(font='上首润黑体.ttf',size=15*2,encoding='utf-8')
    draw.text((20*2,498*2),now_time,font=font_under,fill=(123,123,123))
    #im = im.resize((im.size[0]*10,im.size[1]*10),Image.ANTIALIAS)
    return im

#im = draw_img('哔哩哔哩',['呃呃','呃呃呃呃呃有事吗','啊实打实大苏打实打实的','傲山东黄金哦赛的环境发丝哦见到四度骄傲山东黄金哦赛的环境发丝哦见到四度骄傲山东黄金哦赛哦见到四度骄傲山哦见到四度骄傲山哦见到四度骄傲山哦见到四度骄傲山的环境发丝哦见到四度骄傲山东黄金哦赛的环境四度骄傲山东黄金哦赛的环境','撒打算飞洒发生飞洒发生发生发生','测试'])
#im.show()

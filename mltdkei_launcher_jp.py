# mltdkei Module #
import mltdkei_v40

IDB_name = 'mltdkei_idoldata.sqlite'
MDB_name = 'mltdkei_songdata.sqlite'
info_name = 'mltdkei_info.txt'
SongDB_name = 'name_jp'

if __name__ == '__main__':
    mltdkei_v40.mltdkei_mainframe(IDB_name, MDB_name, info_name, SongDB_name)
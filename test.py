import unittest
import main


class TestMethods(unittest.TestCase):
    def test_unit_constructor(self):
        self.assertTrue(isinstance(main.Swordsman(1, 1), main.Swordsman))
        self.assertTrue(isinstance(main.Archer(1, 1), main.Archer))
        self.assertTrue(isinstance(main.Horseman(1, 1), main.Horseman))
        self.assertTrue(isinstance(main.Lumberjack(1, 1), main.Lumberjack))
        self.assertTrue(isinstance(main.Miner(1, 1), main.Miner))
        self.assertTrue(isinstance(main.Hunter(1, 1), main.Hunter))

    def test_unit_production(self):
        b = main.Barrack(1, 1)
        l = main.LumberjackHut(1, 1)
        m = main.MinerHut(1, 1)
        h = main.HuntersHut(1, 1)
        for i in range(0, 20):
            h._make_unit(h._unit_type[0])
            l._make_unit(l._unit_type[0])
            m._make_unit(m._unit_type[0])
            for j in range(0, 3):
                b._make_unit(b._unit_type[j])

        self.assertEqual(len(h._units), 20)
        self.assertEqual(len(l._units), 20)
        self.assertEqual(len(m._units), 20)
        self.assertEqual(len(b._units), 60)

        for i in range(0, 20):
            self.assertTrue(isinstance(h._units[i], main.Hunter))
            self.assertTrue(isinstance(l._units[i], main.Lumberjack))
            self.assertTrue(isinstance(m._units[i], main.Miner))
            self.assertTrue(isinstance(b._units[i * 3], main.Swordsman))
            self.assertTrue(isinstance(b._units[i * 3 + 1], main.Archer))
            self.assertTrue(isinstance(b._units[i * 3 + 2], main.Horseman))

    def test_unit_kill(self):
        s = main.Swordsman(1, 1)
        a = main.Archer(1, 1)
        hr = main.Horseman(1, 1)
        l = main.Lumberjack(1, 1)
        m = main.Miner(1, 1)
        hn = main.Hunter(1, 1)
        s._destroy()
        a._destroy()
        hr._destroy()
        l._destroy()
        m._destroy()
        hn._destroy()
        self.assertTrue(s._dead)
        self.assertTrue(a._dead)
        self.assertTrue(hr._dead)
        self.assertTrue(l._dead)
        self.assertTrue(m._dead)
        self.assertTrue(hn._dead)

    def test_single_building(self):
        b = main.Barrack(1, 1)
        l = main.LumberjackHut(1, 1)
        m = main.MinerHut(1, 1)
        h = main.HuntersHut(1, 1)
        self.assertEqual(b, main.Barrack(10, 10))
        self.assertEqual(l, main.LumberjackHut(10, 10))
        self.assertEqual(m, main.MinerHut(10, 10))
        self.assertEqual(h, main.HuntersHut(10, 10))

    def test_building_detsroy(self):
        b = main.Barrack(1, 1)
        l = main.LumberjackHut(1, 1)
        m = main.MinerHut(1, 1)
        h = main.HuntersHut(1, 1)
        b._destroy()
        l._destroy()
        m._destroy()
        h._destroy()
        self.assertNotEqual(b, main.Barrack(10, 10))
        self.assertNotEqual(l, main.LumberjackHut(10, 10))
        self.assertNotEqual(m, main.MinerHut(10, 10))
        self.assertNotEqual(h, main.HuntersHut(10, 10))


unittest.main()